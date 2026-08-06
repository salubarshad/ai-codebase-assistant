from pathlib import Path
from collections.abc import Iterator

from config import PROJECT_ROOT, IGNORED


def resolve_project_path(path: str) -> Path:
    resolved_path = (PROJECT_ROOT / Path(path)).resolve()

    if not resolved_path.is_relative_to(PROJECT_ROOT):
        raise Exception("Access restricted.")
    if not resolved_path.exists():
        raise Exception(f"Path does not exist.")

    return resolved_path


def list_files(path: str = ".") -> list[dict]:
    resolved_path = resolve_project_path(path)

    if not resolved_path.is_dir():
        raise Exception(f"Not a directory.")

    items = []
    for item in resolved_path.iterdir():
        if item.name not in IGNORED:
            items.append(
                {
                    "name": item.name,
                    "path": str(item.relative_to(PROJECT_ROOT)),
                    "type": "file" if item.is_file() else "directory",
                    "extension": item.suffix if item.is_file() else None,
                }
            )

    items.sort(
        key=lambda item: (
            item["type"] != "directory",
            item["name"],
        )
    )

    return items


def read_file(path: str) -> str:
    resolved_path = resolve_project_path(path)

    if not resolved_path.is_file():
        raise Exception(f"Not a file.")

    try:
        file_content = resolved_path.read_text(encoding="utf-8")
    except Exception as e:
        raise RuntimeError(f"Error reading '{resolved_path}': {e}") from e

    lines = file_content.splitlines(keepends=False)
    numbered_lines = []
    width = len(str(len(lines)))
    for i, line in enumerate(lines, start=1):
        numbered_lines.append(f"{i:>{width}} | {line}")

    return "\n".join(numbered_lines)


def iter_project_files(path: Path) -> Iterator[Path]:
    for file in path.iterdir():
        if file.name not in IGNORED:
            if file.is_file():
                yield file
            elif file.is_dir():
                yield from iter_project_files(file)


def search_file(query: str, file: Path) -> list[dict]:
    try:
        lines = file.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return []

    matching_lines = []
    for i, line in enumerate(lines, start=1):
        if query in line:
            matching_lines.append(
                {
                    "line": i,
                    "content": line.strip(),
                }
            )

    return matching_lines


def search_codebase(query: str, path: str) -> list[dict]:
    resolved_path: Path = resolve_project_path(path)

    matching_lines: list[dict] = []
    for file in iter_project_files(resolved_path):
        matches = search_file(query, file)
        for match in matches:
            matching_lines.append(
                {
                    "file": str(file.relative_to(PROJECT_ROOT)),
                    "line": match["line"],
                    "content": match["content"],
                }
            )

    return matching_lines


def get_project_name():
    return "AI Codebase Assistant"


def add_numbers(a: int, b: int) -> int:
    return a + b
