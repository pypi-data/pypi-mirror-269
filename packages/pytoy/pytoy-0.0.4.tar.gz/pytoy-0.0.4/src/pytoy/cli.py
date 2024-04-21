from nginx import Nginx
import cli_file
import common
import fire
import json
import os
import re

class CLI(object):
    """PyToy CLI."""

    def path(self) -> str:
        """Get PyToy path."""
        return os.path.dirname(os.path.abspath(__file__))

    def version(self) -> str:
        """Get PyToy version."""
        path = common.find_file_by_pattern(
            os.path.dirname(self.path()) + "/pytoy-*.dist-info"
        )
        return re.findall(r"pytoy-(.*).dist-info", path)[0] if path else "0.0.0"

    class nginx(Nginx):
        pass

    def ls(
        self, dir: str = ".", max_depth: int | None = 1, indent: int | str | None = None
    ):
        """List directory."""
        return json.dumps(cli_file.list_file_structure(dir, max_depth), indent=indent)

    def replace_file(self, file: str, old: str, new: str, extension: str = None):
        if extension and not file.endswith(extension):
            return
        with open(file, "r") as f:
            text = f.read()
        text = text.replace(old, new)
        with open(file, "w") as f:
            f.write(text)

    def replace_dir(
        self,
        dir: str,
        old: str,
        new: str,
        extension: str = None,
        recursive: bool = False,
    ):
        for root, dirs, files in os.walk(dir):
            for file in files:
                file_path = os.path.join(root, file)
                self.replace_file(file_path, old, new, extension)

            if not recursive:
                break

            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                self.replace_dir(subdir_path, old, new, extension, recursive)


def PyToy():
    fire.Fire(CLI)


if __name__ == "__main__":
    PyToy()
