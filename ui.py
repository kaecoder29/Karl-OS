"""ui.py - all terminal output styling lives here so MiniOS looks consistent."""
import os

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def enable_colors():
    """Windows CMD (10+) needs this once to understand ANSI color codes."""
    if os.name == "nt":
        os.system("")


def error(msg):
    print(f"{RED}{msg}{RESET}")


def ok(msg):
    print(f"{GREEN}{msg}{RESET}")


def warn(msg):
    print(f"{YELLOW}{msg}{RESET}")


def info(msg):
    print(f"{CYAN}{msg}{RESET}")


def prompt_text(user, cwd):
    return f"{GREEN}{user}@minios{RESET}:{CYAN}{cwd}{RESET}$ "
