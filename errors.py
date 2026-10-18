class MiniOSError(Exception):
    """Base class for all expected MiniOS errors."""


class UsageError(MiniOSError):
    """Command was called with wrong/missing arguments."""


class PermissionDenied(MiniOSError):
    """User is not allowed to perform this action."""


class OutOfMemory(MiniOSError):
    """Memory manager could not satisfy an allocation."""


class InvalidPID(MiniOSError):
    """No process exists with the given PID."""


class FileSystemError(MiniOSError):
    """File not found, already exists, not a directory, etc."""


class AuthError(MiniOSError):
    """Login failed or user does not exist."""
