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
                return list(), set()
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

    metadata = item.stat()
    # permissions = stat.filemode(metadata.st_mode)
    # modified_mtime = datetime.fromtimestamp(metadata.st_mtime)
    # # modified_atime = datetime.fromtimestamp(metadata.st_atime)
    # # modified_ctime = datetime.fromtimestamp(metadata.st_ctime)
    # owner = pwd.getpwuid(metadata.st_uid).pw_name
    # group = grp.getgrgid(metadata.st_gid).gr_name
    # size = metadata.st_size
    # hard_links = metadata.st_nlink

    info = FileInfo(
        permissions=stat.filemode(metadata.st_mode),
        owner=pwd.getpwuid(metadata.st_uid).pw_name,
        group=grp.getgrgid(metadata.st_gid).gr_name,
        size=metadata.st_size,
        hard_links=metadata.st_nlink,
        modified_mtime=datetime.fromtimestamp(metadata.st_mtime),
        # modified_atime=modified_atime,
        # modified_ctime=modified_ctime
    )

    return info


def format_long_listing(item: Path):
    metadata = get_metadata(item)
    print(
        f"{metadata.permissions} "
        f"{metadata.hard_links} "
        f"{metadata.owner} "
        f"{metadata.group} "
        f"{metadata.size:>6} "
        f"{metadata.modified_mtime}",
        end=" ",
    )


def list_directories(valid_paths: list[Path], flags: set[str]) -> None:

    for path in valid_paths:
        if len(valid_paths) > 1:
            print(f"{path}:")
        for item in sorted(path.iterdir(), key=lambda item: item.name.lower()):
            if "-a" not in flags and item.name.startswith("."):
                continue
            if "-l" in flags:
                format_long_listing(item=item)
            if item.is_dir():
                print(f"{BLUE}{item.name}{RESET}")
            else:
                print(item.name)

        print()


def main() -> int:
    paths, flags = parse_args(sys.argv[1:])

    if not paths:
        return 1

    valid_paths = validate_paths(paths)

    if not valid_paths:
        return 1

    list_directories(valid_paths, flags)

    return 0


if __name__ == "__main__":
    sys.exit(main())
