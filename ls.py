from pathlib import Path
import sys

BLUE = "\033[34m"
RESET = "\033[0m"
DIR_PREFIX = "d "
FILE_PREFIX = "- "


def main() -> None:
    if len(sys.argv) == 2:
        path = Path(sys.argv[1])
    elif len(sys.argv) == 1:
        path = Path(".")
    else:
        print("Too many args given!")
        return

    if not path.exists():
        print("Path Doesn't Exist")
        return

    if not path.is_dir():
        print("Path Must Be A Directory")
        return

    for item in sorted(path.iterdir(), key=lambda item: item.name.lower()):
        if item.is_dir():
            print(f"{BLUE}{DIR_PREFIX}{item.name}{RESET}")
        else:
            print(f"{FILE_PREFIX}{item.name}")


if __name__ == "__main__":
    main()
