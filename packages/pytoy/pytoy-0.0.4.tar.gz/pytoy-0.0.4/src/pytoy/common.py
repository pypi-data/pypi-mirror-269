import glob
import os


def run_command_str(cmd: str):
    """Run a command as a string."""
    return os.popen(cmd).read().strip()


def find_file_by_pattern(pattern):
    """Find a file by pattern."""
    list_files = glob.glob(pattern)
    return list_files[0] if len(list_files) > 0 else None