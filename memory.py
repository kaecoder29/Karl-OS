"""memory.py - simulated memory manager for MiniOS."""
from errors import OutOfMemory, InvalidPID


class MemoryManager:
    def __init__(self, total_mb=69420):
        self.total = total_mb
        self.allocations = {}          # {pid: mb}

    @property
    def used(self):
        return sum(self.allocations.values())

    @property
    def free_mb(self):
        return self.total - self.used

    def allocate(self, pid, mb):
        if mb > self.free_mb:
            raise OutOfMemory(
                f"requested {mb} MB but only {self.free_mb} MB is free")
        self.allocations[pid] = self.allocations.get(pid, 0) + mb

    def free(self, pid):
        if pid not in self.allocations:
            raise InvalidPID(f"PID {pid} has no allocated memory")
        return self.allocations.pop(pid)