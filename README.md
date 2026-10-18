# KarlOS

## 1. Project Name

**KarlOS** — Mini Operating System (MiniOS)

## 2. Group Members

1. Karl Frederick Sitjar
2. Ritchie Conrad Hoo
3. Zenadine Zidane Pablo
4. Juncel Loriosa
5. Danica Grace Perjes

## 3. Project Description

KarlOS is a Python-based Mini Operating System simulation developed for academic purposes. It demonstrates basic operating system concepts through a command-line interface (CLI). Users can enter commands to interact with a simulated environment that represents system information, file and directory management, process management, and memory management.

KarlOS runs as a Python application on an existing operating system. Its process and memory management functions are simulations and do not directly control the host computer's actual processes or physical memory.

## 4. Features

- Command-line interface for user interaction
- System information and utility commands
- Simulated file and directory management
- Simulated process management
- Simulated memory allocation and release
- Command history and help functionality
- Basic command validation and error handling

*Note: These features are based on the technical documentation and should be verified against the implemented source code.*

## 5. Requirements

- Python 3
- Windows, Linux, or macOS
- Command Prompt, PowerShell, or Terminal
- A text editor or IDE, such as Visual Studio Code

## 6. How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run the main Python file:

```bash
python main.py
```

Replace `main.py` with the actual entry-point filename if your project uses a different name.

## 7. Available Commands

### General and System Commands

| Command | Description |
|---|---|
| `help` | Displays available commands or help for a specific command. |
| `whoami` | Displays the simulated current user identity. |
| `date` | Displays date-related information. |
| `uptime` | Shows how long the application has been running. |
| `systeminfo` | Displays general information about the simulated system. |
| `clear` | Clears the terminal display. |
| `history` | Displays previously entered commands. |
| `history -c` | Clears command history, if supported. |
| `exit` | Exits KarlOS. |

### File and Directory Management Commands

| Command | Description |
|---|---|
| `mkdir <directory_name>` | Creates a directory. |
| `ls [path]` | Lists files and directories. |
| `cd <path>` | Changes the current directory. |
| `pwd` | Displays the current working directory. |
| `create <filename> [text]` | Creates a file and optionally adds text. |
| `cat <filename>` | Displays the contents of a text file. |
| `del <name>` | Deletes a file or directory, depending on the implementation. |

### Process Management Commands

| Command | Description |
|---|---|
| `process` | Displays simulated process information. |
| `run <process_name>` | Starts or simulates a process. |
| `kill <PID>` | Terminates a simulated process using its process ID. |

### Memory Management Commands

| Command | Description |
|---|---|
| `memory` | Displays simulated memory information. |
| `allocate <PID> <amount_in_MB>` | Allocates simulated memory to a process. |
| `free <PID>` | Releases simulated memory associated with a process. |

**Note:** Commands and optional arguments listed above are based on the technical documentation. Their availability and exact syntax should be confirmed against the actual Python implementation.

## 8. Project Files

The repository may contain the following project deliverables:

- **Python Source Code** — Implementation of KarlOS.
- **README.md** — Project overview, requirements, and command reference.
- **Technical Documentation** — System design, specifications, testing, and limitations.
- **User Manual** — Instructions for using KarlOS.
- **Screenshots** — Evidence of the program running and its commands in use.
- **Individual Reports** — Reports describing group members' contributions.

## 9. Project Objectives

- Demonstrate fundamental Python programming concepts.
- Simulate selected operating system functions through a CLI.
- Implement commands for system information and file management.
- Demonstrate simulated process and memory management.
- Practice command validation, error handling, and version control.

## 10. Limitations

- KarlOS runs within an existing operating system and is not a standalone bootable OS.
- Process management is simulated and does not necessarily manage real operating system processes.
- Memory management is simulated and does not directly control physical RAM.
- File and directory persistence depends on the implementation.
- The available command set is limited to the functions implemented in the project.

## 11. Acknowledgment

Developed as an academic group project in partial fulfillment of the course requirements.