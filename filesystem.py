from errors import FileSystemError


class FileSystem:
    def __init__(self):
        self.root = {}   # {"docs": {"notes.txt": "hello"}, "bin": {}}

    # ---------- helpers ----------
    def _split(self, path, cwd):
        """Turn any path into a clean list of names.
        '/a/b/../c' -> ['a', 'c'];  'x' with cwd '/home' -> ['home', 'x']"""
        if not path.startswith("/"):
            path = cwd.rstrip("/") + "/" + path
        parts = []
        for p in path.split("/"):
            if p in ("", "."):
                continue
            if p == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(p)
        return parts

    def _get(self, parts):
        """Walk down the tree and return the node at that location."""
        node = self.root
        for name in parts:
            if not isinstance(node, dict) or name not in node:
                raise FileSystemError(f"no such file or directory: /{'/'.join(parts)}")
            node = node[name]
        return node

    # ---------- public operations ----------
    def normalize(self, path, cwd):
        return "/" + "/".join(self._split(path, cwd))

    def is_dir(self, path, cwd):
        try:
            return isinstance(self._get(self._split(path, cwd)), dict)
        except FileSystemError:
            return False

    def mkdir(self, path, cwd):
        parts = self._split(path, cwd)
        if not parts:
            raise FileSystemError("cannot create the root directory")
        parent = self._get(parts[:-1])
        if not isinstance(parent, dict):
            raise FileSystemError(f"not a directory: /{'/'.join(parts[:-1])}")
        name = parts[-1]
        if name in parent:
            raise FileSystemError(f"'{name}' already exists")
        parent[name] = {}

    def ls(self, path, cwd):
        """Return a sorted list of (name, is_directory)."""
        node = self._get(self._split(path, cwd))
        if not isinstance(node, dict):
            raise FileSystemError(f"not a directory: {path}")
        return sorted((n, isinstance(v, dict)) for n, v in node.items())
    
    def create(self, path, cwd, content=""):
        parts = self._split(path, cwd)
        if not parts:
            raise FileSystemError("invalid file name")
        parent = self._get(parts[:-1])
        if not isinstance(parent, dict):
            raise FileSystemError(f"not a directory: /{'/'.join(parts[:-1])}")
        name = parts[-1]
        if name in parent:
            raise FileSystemError(f"'{name}' already exists")
        parent[name] = content      # a string = a file


    def read(self, path, cwd):
        node = self._get(self._split(path, cwd))
        if isinstance(node, dict):
            raise FileSystemError(f"'{path}' is a directory, not a file")
        return node

    def remove(self, path, cwd):
        parts = self._split(path, cwd)
        if not parts:
            raise FileSystemError("cannot delete the root directory")
        parent = self._get(parts[:-1])
        name = parts[-1]
        if not isinstance(parent, dict) or name not in parent:
            raise FileSystemError(f"no such file or directory: {path}")
        if isinstance(parent[name], dict) and parent[name]:
            raise FileSystemError(f"'{path}' is not empty")
        del parent[name]