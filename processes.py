import time
from errors import InvalidPID, PermissionDenied


class Process:
    def __init__(self, pid, name, user):
        self.pid = pid
        self.name = name
        self.user = user
        self.state = "RUNNING"
        self.started = time.time()

    def age_seconds(self):
        return int(time.time() - self.started)


class ProcessManager:
    def __init__(self):
        self.table = {}        # {pid: Process}
        self.next_pid = 1
        self.start("init", "root")      # PID 1, protected

    def start(self, name, user):
        proc = Process(self.next_pid, name, user)
        self.table[proc.pid] = proc
        self.next_pid += 1
        return proc

    def kill(self, pid):
        if pid not in self.table:
            raise InvalidPID(f"no process with PID {pid}")
        if pid == 1:
            raise PermissionDenied("cannot kill init (PID 1)")
        return self.table.pop(pid)

    def list(self):
        return [self.table[pid] for pid in sorted(self.table)]