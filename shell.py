import os
import shlex
from datetime import datetime

import ui
from errors import MiniOSError, UsageError, InvalidPID

from filesystem import FileSystem
from errors import MiniOSError, UsageError, FileSystemError

COMMANDS = {}
ALIASES = {
    "dir": "ls",
    "cls": "clear",
    "del": "rm",
    "type": "cat",
    "md": "mkdir",
    "quit": "exit",
    "logout": "exit",   
    "ver": "version",
}

CATEGORY_ORDER = ["Users", "System", "File Management", "Process Management", "Memory Management",]


def command(name, description="", usage=None, category="System"):
    def decorator(func):
        COMMANDS[name] = {
            "func": func,
            "desc": description,
            "usage": usage or name,
            "category": category,
        }
        return func
    return decorator


def require_args(args, minimum, usage, maximum=None):
    too_few = len(args) < minimum
    too_many = maximum is not None and len(args) > maximum
    if too_few or too_many:
        raise UsageError(f"usage: {usage}")


def parse(line):
    parts = shlex.split(line)
    return parts[0], parts[1:]


def resolve(name):
    name = name.lower()
    return ALIASES.get(name, name)




@command("help", "List commands, or show details for one",
         usage="help [command]")
def cmd_help(kernel, args):
    require_args(args, 0, "help [command]", maximum=1)

    if args:
        name = resolve(args[0])
        entry = COMMANDS.get(name)
        if not entry:
            raise MiniOSError(f"no help available for '{args[0]}'")
        print(f"{ui.BOLD}{name}{ui.RESET} - {entry['desc']}")
        print(f"  usage:    {entry['usage']}")
        print(f"  category: {entry['category']}")
        aliases = [a for a, real in ALIASES.items() if real == name]
        if aliases:
            print(f"  aliases:  {', '.join(sorted(aliases))}")
        return

    categories = [c for c in CATEGORY_ORDER
                  if any(e["category"] == c for e in COMMANDS.values())]
    extras = sorted({e["category"] for e in COMMANDS.values()}
                    - set(CATEGORY_ORDER))

    for i, cat in enumerate(categories + extras):
        if i > 0:
            print()                      # blank line between groups
        print(f"{ui.BOLD}{ui.CYAN}{cat}{ui.RESET}")
        for name in sorted(n for n, e in COMMANDS.items()
                           if e["category"] == cat):
            print(f"  {name:<10} {COMMANDS[name]['desc']}")
    print("\nType 'help <command>' for details.")


@command("whoami", "Show the current user", category="Users")
def cmd_whoami(kernel, args):
    print(kernel.current_user)


@command("date", "Show the current date and time")
def cmd_date(kernel, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@command("uptime", "Show how long MiniOS has been running")
def cmd_uptime(kernel, args):
    secs = kernel.uptime_seconds()
    print(f"Up for {secs // 60} min {secs % 60} sec")


@command("systeminfo", "Show its system information")
def cmd_version(kernel, args):
    print(f"OS Name: KarlOS Halimaw ")
    print(f"Version: 0.69")
    print("Architecture: 128-bit")
    print("CPU: SELOSO")
    print("MEMORY: 8210MB")
    print("User: Bot ah")


@command("clear", "Clear the screen")
def cmd_clear(kernel, args):
    os.system("cls" if os.name == "nt" else "clear")


@command("history", "Show previously entered commands",
         usage="history [-c]")
def cmd_history(kernel, args):
    require_args(args, 0, "history [-c]", maximum=1)
    if args == ["-c"]:
        kernel.history.clear()
        ui.ok("History cleared.")
        return
    for i, line in enumerate(kernel.history, 1):
        print(f"  {i:>3}  {line}")


@command("exit", "Shut down MiniOS")
def cmd_exit(kernel, args):
    kernel.running = False
    ui.info("Shutting down MiniOS...")



def execute(kernel, line):
    name, args = parse(line)
    name = resolve(name)
    entry = COMMANDS.get(name)
    if entry is None:
        raise MiniOSError(f"{name}: command not found (type 'help')")
    entry["func"](kernel, args)


def run_shell(kernel):
    while kernel.running:
        try:
            line = input(ui.prompt_text(kernel.current_user, kernel.cwd)).strip()
            if not line:
                continue
            kernel.history.append(line)
            execute(kernel, line)

        except MiniOSError as e:         
            ui.error(f"Error: {e}")
        except ValueError as e:          
            ui.error(f"Parse error: {e}")
        except KeyboardInterrupt:        
            print()
            ui.warn("Use 'exit' to shut down.")
        except EOFError:                 
            print()
            ui.warn("Use 'exit' to shut down.")
        except Exception as e:           
            ui.error(f"Internal error ({type(e).__name__}): {e}")

#FILE SYSTEM COMMANDS

@command("mkdir", "Create a directory", usage="mkdir <name> [name...]", category="File Management")
def cmd_mkdir(kernel, args):
    require_args(args, 1, "mkdir <name> [name...]")
    for name in args:
        kernel.fs.mkdir(name, kernel.cwd)


@command("ls", "List directory contents", usage="ls [path]", category="File Management")
def cmd_ls(kernel, args):
    require_args(args, 0, "ls [path]", maximum=1)
    path = args[0] if args else "."
    for name, is_dir in kernel.fs.ls(path, kernel.cwd):
        if is_dir:
            print(f"{ui.CYAN}{name}/{ui.RESET}")
        else:
            print(name)


@command("cd", "Change directory", usage="cd <path>", category="File Management")
def cmd_cd(kernel, args):
    require_args(args, 1, "cd <path>", maximum=1)
    if not kernel.fs.is_dir(args[0], kernel.cwd):
        raise FileSystemError(f"not a directory: {args[0]}")
    kernel.cwd = kernel.fs.normalize(args[0], kernel.cwd)


@command("pwd", "Print the current directory", category="File Management")
def cmd_pwd(kernel, args):
    print(kernel.cwd)


@command("create", "Create a file, optionally with text",
         usage="create <file> [text...]", category="File Management")
def cmd_create(kernel, args):
    require_args(args, 1, "create <file> [text...]")
    content = " ".join(args[1:])
    kernel.fs.create(args[0], kernel.cwd, content)


@command("cat", "Show the contents of a file",
         usage="cat <file>", category="File Management")
def cmd_cat(kernel, args):
    require_args(args, 1, "cat <file>", maximum=1)
    print(kernel.fs.read(args[0], kernel.cwd))


@command("del", "Delete a file or empty directory",
         usage="del <name> [name...]", category="File Management")
def cmd_rm(kernel, args):
    require_args(args, 1, "del <name> [name...]")
    for name in args:
        kernel.fs.remove(name, kernel.cwd)

#PROCESS MANAGEMENT COMMANDS

@command("process", "List running processes",
         usage="process", category="Process Management")
def cmd_process(kernel, args):
    require_args(args, 0, "process", maximum=0)
    print(f"{ui.BOLD}{'PID':<6}{'USER':<10}{'STATE':<10}{'TIME':<8}NAME{ui.RESET}")
    for p in kernel.processes.list():
        print(f"{p.pid:<6}{p.user:<10}{ui.GREEN}{p.state:<10}{ui.RESET}"
              f"{p.age_seconds():<8}{p.name}")

@command("run", "Start a new process",
         usage="run <name>", category="Process Management")
def cmd_run(kernel, args):
    require_args(args, 1, "run <name>", maximum=1)
    proc = kernel.processes.start(args[0], kernel.current_user)
    ui.ok(f"Started '{proc.name}' with PID {proc.pid}")


@command("kill", "Terminate a process by PID",
         usage="kill <pid>", category="Process Management")
def cmd_kill(kernel, args):
    require_args(args, 1, "kill <pid>", maximum=1)
    if not args[0].isdigit():
        raise UsageError("usage: kill <pid> (PID must be a number)")
    proc = kernel.processes.kill(int(args[0]))
    if proc.pid in kernel.memory.allocations:
        kernel.memory.free(proc.pid)
    ui.ok(f"Killed '{proc.name}' (PID {proc.pid})")

#MEMORY MANAGEMENT

@command("memory", "Show memory status",
         usage="memory", category="Memory Management")
def cmd_memory(kernel, args):
    require_args(args, 0, "memory", maximum=0)
    m = kernel.memory
    print("\nMemory Status")
    print("-" * 24)
    print(f"{'Total Memory:':<14}{m.total:>4} MB")
    print(f"{'Used Memory:':<14}{m.used:>4} MB")
    print(f"{'Free Memory:':<14}{m.free_mb:>4} MB")
    if m.allocations:
        print(f"\n{ui.BOLD}{'PID':<6}{'NAME':<12}USED{ui.RESET}")
        for pid, mb in sorted(m.allocations.items()):
            proc = kernel.processes.table.get(pid)
            name = proc.name if proc else "?"
            print(f"{pid:<6}{name:<12}{mb} MB")


@command("allocate", "Allocate memory (MB) to a process",
         usage="allocate <pid> <mb>", category="Memory Management")
def cmd_allocate(kernel, args):
    require_args(args, 2, "allocate <pid> <mb>", maximum=2)
    if not (args[0].isdigit() and args[1].isdigit()):
        raise UsageError("usage: allocate <pid> <mb> (both must be numbers)")
    pid, mb = int(args[0]), int(args[1])
    if mb <= 0:
        raise UsageError("amount must be greater than 0")
    if pid not in kernel.processes.table:
        raise InvalidPID(f"no process with PID {pid}")
    kernel.memory.allocate(pid, mb)
    ui.ok(f"Allocated {mb} MB to PID {pid}")


@command("free", "Free all memory held by a process",
         usage="free <pid>", category="Memory Management")
def cmd_free(kernel, args):
    require_args(args, 1, "free <pid>", maximum=1)
    if not args[0].isdigit():
        raise UsageError("usage: free <pid> (PID must be a number)")
    mb = kernel.memory.free(int(args[0]))
    ui.ok(f"Freed {mb} MB from PID {args[0]}")

