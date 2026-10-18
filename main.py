import time

import ui
from kernel import Kernel
from shell import run_shell


def boot():
    print(f"{ui.BOLD}{ui.RED}" + "=" * 40)
    print("         KarlOS Halimaw sa Kama")
    print("=" * 40 + ui.RESET)
    print("Welcome to KarlOS")



def main():
    ui.enable_colors()
    boot()
    kernel = Kernel()
    print("Type 'help' to see available commands.\n")
    run_shell(kernel)


if __name__ == "__main__":
    main()
