# Unix ls Clone

A Python implementation of the Unix ls command supporting recursive directory traversal, long-format listings, hidden files, and colored output.
---

## Features

- List directory contents
- Recursive directory listing (`-R`)
- Long listing format (`-l`)
- Show hidden files (`-a`)
- Support combined flags (`-la`, `-al`, etc.)
- Colored directory output
- Human-readable, well-structured code

---

## Technologies Used

- Python 3.13
- pathlib
- dataclasses
- datetime
- pwd
- grp
- stat

---

## Project Structure

```text
.
├── ls.py
├── README.md
├── pyproject.toml
└── ...
```
---

## Usage

Clone the repository:

```bash
git clone https://github.com/amragazia/unix-ls-clone.git
cd unix-ls-clone
```

Run:

```bash
python ls.py
```

Examples:

```bash
python ls.py
python ls.py -l
python ls.py -a
python ls.py -R
python ls.py -l -a -R
python ls.py /home/peter
```

---

## Supported Flags

| Flag | Description |
|------|-------------|
| `-a` | Show hidden files |
| `-l` | Long listing format |
| `-R` | Recursive listing |

---


## Skills Demonstrated

- Python
- Object-Oriented Programming
- Recursion
- pathlib
- File System APIs
- Command-Line Interface (CLI)
- Git
- GitHub


## Future Improvements

- Human-readable file sizes (`-h`)
- Sorting options
- Better argument parsing with `argparse`
- Symlink support
- Better error handling

---

## License

MIT