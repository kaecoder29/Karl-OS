"""kernel.py - central state shared by every MiniOS subsystem."""
from filesystem import FileSystem
import time
from processes import ProcessManager 
from memory import MemoryManager


class Kernel:
    def __init__(self):
        self.boot_time = time.time()
        self.running = True
        self.current_user = "KarlitoBoy"
        self.cwd = "/"
        self.history = []          # every command line the user has typed
        self.fs = FileSystem()
        self.processes = ProcessManager() 
        self.memory = MemoryManager(total_mb=69420) 

    def uptime_seconds(self):
        return int(time.time() - self.boot_time)
