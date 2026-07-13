from pathlib import Path
import sys

BLUE = "\033[34m"
RESET = "\033[0m"
DIR_PREFIX = "d "
FILE_PREFIX = "- "


def parse_args(args: list[str]) -> tuple[list[Path], set[str]]:
    valid_options: set[str] = {"-a", "-l", "-R", "-h"}
    options: set[str] = set()
    paths: list[Path] = []
    for arg in args:
        if arg.startswith("-"):
            if arg not in valid_options:
                print(f"ls: invalid option -- '{arg}'", file=sys.stderr)
                sys.exit(1)
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
            print("Error: Path Must Be A Directory", file=sys.stderr)
            continue

        valid_paths.append(path)

    if not valid_paths:
        return []

    return valid_paths


def list_directory(valid_paths: list[Path], flags: set[str]) -> None:

    # flags not applied yet 

    for path in valid_paths:
        print(f"{path}:")
        for item in sorted(path.iterdir(), key=lambda item: item.name.lower()):
            if "-a" not in flags and item.name.startswith("."):
                continue
            if item.is_dir():
                print(f"{BLUE}{DIR_PREFIX}{item.name}{RESET}")
            else:
                print(f"{FILE_PREFIX}{item.name}")

        print("\n")


def main() -> int:
    paths, flags = parse_args(sys.argv[1:])

    if not paths:
        return 1

    valid_paths = validate_paths(paths)

    if not valid_paths:
        return 1

    list_directory(valid_paths, flags)

    return 0


if __name__ == "__main__":
    sys.exit(main())
