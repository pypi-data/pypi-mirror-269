import os


def walk(dir, max_depth: int | None = 1):
    """Walk a directory up to a maximum depth."""
    if max_depth is None:
        return os.walk(dir)
    dir = os.path.abspath(dir)
    prefix_len = len(dir.split(os.sep))

    for root, dirs, files in os.walk(dir):
        depth = len(root.split(os.sep)) - prefix_len
        if depth < max_depth:
            yield root, dirs, files
        else:
            del dirs[:]


def list_file_structure(dir: str = ".", max_depth: int | None = 1):
    """List directory."""
    file_structure = {}

    for root, dirs, files in walk(dir, max_depth):
        for file in files:
            path = os.path.join(root, file)
            file_structure[path] = {
                "size": os.path.getsize(path),
                "last_modified": os.path.getmtime(path),
            }

    return file_structure
