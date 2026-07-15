from pathlib import Path
import sys
from dataclasses import dataclass
import stat
from datetime import datetime
import pwd
import grp

BLUE = "\033[34m"
RESET = "\033[0m"


def parse_args(args: list[str]) -> tuple[list[Path], set[str]]:
    valid_options: set[str] = {"-a", "-l", "-R", "-h"}
    options: set[str] = set()
    paths: list[Path] = []
    for arg in args:
        if arg.startswith("-"):
            if arg not in valid_options:
                print(f"ls: invalid option -- '{arg}'", file=sys.stderr)
                return [], set()
            options.add(arg)
            continue
        path = Path(arg)
        paths.append(path)

    if not paths:
        paths.append(Path("."))

    return paths, options


def validate_paths(paths: list[Path]) -> list[Path]:

    valid_paths: list[Path] = []

    for path in paths:
        if not path.exists():
            print(f"Error: '{path}' does not exist.", file=sys.stderr)
            continue

        if not path.is_dir():
            print(f"Error: '{path}' Must Be A Directory", file=sys.stderr)
            continue

        valid_paths.append(path)

    return valid_paths


@dataclass
class FileInfo:
    permissions: str
    owner: str
    group: str
    size: int
    hard_links: int
    modified_mtime: datetime
    # modified_atime: datetime
    # modified_ctime: datetime


def get_metadata(item: Path) -> FileInfo:

    stat_result = item.stat()

    return FileInfo(
        permissions=stat.filemode(stat_result.st_mode),
        owner=pwd.getpwuid(stat_result.st_uid).pw_name,
        group=grp.getgrgid(stat_result.st_gid).gr_name,
        size=stat_result.st_size,
        hard_links=stat_result.st_nlink,
        modified_mtime=datetime.fromtimestamp(stat_result.st_mtime),
        # modified_atime=datetime.fromtimestamp(stat_result.st_atime),
        # modified_ctime=datetime.fromtimestamp(stat_result.st_ctime)
    )


def format_long_listing(item: Path) -> str:
    metadata = get_metadata(item)
    return (
        f"{metadata.permissions} "
        f"{metadata.hard_links} "
        f"{metadata.owner} "
        f"{metadata.group} "
        f"{metadata.size:>6} "
        f"{metadata.modified_mtime:%b %d %H:%M}"
    )


def format_name(item: Path) -> str:
    if item.is_dir():
        return f"{BLUE}{item.name}{RESET}"

    return item.name


def list_directories(path: Path, flags: set[str], print_header: bool = False) -> None:
    if print_header:    
        print(f"{path}:")

    items = sorted(path.iterdir(), key=lambda item: item.name.lower())

    # Print the contents of the current directory
    for item in items:
        if "-a" not in flags and item.name.startswith("."):
            continue
        if "-l" in flags:
            print(format_long_listing(item=item), end=" ")

        print(format_name(item=item))

    # Handle recursive diving into subdirectories
    for item in items:
        if "-R" in flags and item.is_dir():
            if "-a" not in flags and item.name.startswith("."):
                continue
            print()
            list_directories(item, flags, print_header=True)


def manage_list_directories(valid_paths: list[Path], flags: set[str]) -> None:

    multiple_path = len(valid_paths) > 1

    for i, path in enumerate(valid_paths):
        # Print a blank line between different root directories for readability
        if i > 0: 
            print()

        list_directories(path, flags, print_header=multiple_path)


def main() -> int:
    paths, flags = parse_args(sys.argv[1:])

    if not paths:
        return 1

    valid_paths = validate_paths(paths)

    if not valid_paths:
        return 1

    manage_list_directories(valid_paths, flags)

    return 0


if __name__ == "__main__":
    sys.exit(main())
