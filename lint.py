#!/usr/bin/env python3
"""Linter for Connect Four CLI project.

Enforces:
1. Every source file lives in exactly one layer directory.
2. Imports respect the forward dependency direction.
3. No file exceeds 300 lines.
"""

import ast
import sys
from pathlib import Path

# Layer dependency rules: each layer may import from these layers
ALLOWED_IMPORTS = {
    "types": ["types"],
    "config": ["types", "config"],
    "utils": ["utils"],
    "providers": ["types", "config", "utils", "providers"],
    "repo": ["types", "config", "repo"],
    "service": ["types", "config", "repo", "providers", "service"],
    "runtime": ["types", "config", "repo", "service", "providers", "runtime"],
    "ui": ["types", "config", "service", "runtime", "providers", "ui"],
}

LAYERS = list(ALLOWED_IMPORTS.keys())
SRC_DIR = Path(__file__).parent / "src"


def get_layer(file_path: Path) -> str | None:
    """Return the layer name for a file, or None if not in a layer."""
    try:
        rel_path = file_path.relative_to(SRC_DIR)
        parts = rel_path.parts
        if parts and parts[0] in LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imports(file_path: Path) -> list[str]:
    """Extract import statements from a Python file."""
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except (SyntaxError, UnicodeDecodeError):
        pass
    return imports


def check_line_count(file_path: Path) -> list[tuple[int, str]]:
    """Check if file exceeds 300 lines."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > 300:
            errors.append((301, f"File exceeds 300 lines ({len(lines)} lines)"))
    except UnicodeDecodeError:
        errors.append((1, "Cannot read file as UTF-8"))
    return errors


def check_imports(file_path: Path, layer: str) -> list[tuple[int, str]]:
    """Check that imports respect layer dependency rules."""
    errors = []
    allowed = ALLOWED_IMPORTS[layer]
    imports = get_imports(file_path)

    # Also check for internal imports (from src.module import ...)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                # Check if it's an internal import (starts with src.)
                if node.module.startswith("src."):
                    # Extract the layer from the import
                    parts = node.module.split(".")
                    if len(parts) > 1:
                        imported_layer = parts[1]
                        if imported_layer not in allowed:
                            errors.append(
                                (node.lineno, f"Import from '{imported_layer}' not allowed in '{layer}' layer. May import from: {', '.join(allowed)}")
                            )
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    if module == "src":
                        # Check the next part for layer
                        for n in ast.walk(node):
                            if isinstance(n, ast.alias) and n.name.startswith("src."):
                                parts = n.name.split(".")
                                if len(parts) > 1:
                                    imported_layer = parts[1]
                                    if imported_layer not in allowed:
                                        errors.append(
                                            (node.lineno, f"Import from '{imported_layer}' not allowed in '{layer}' layer. May import from: {', '.join(allowed)}")
                                        )
    except SyntaxError:
        pass

    return errors


def check_file(file_path: Path) -> list[tuple[int, str]]:
    """Check a single file for linting errors."""
    errors = []

    # Check line count
    errors.extend(check_line_count(file_path))

    # Get layer and check imports
    layer = get_layer(file_path)
    if layer:
        errors.extend(check_imports(file_path, layer))

    return errors


def main() -> int:
    """Run linter on all Python files in src/."""
    all_errors = []

    # Find all Python files in src/
    for py_file in SRC_DIR.rglob("*.py"):
        errors = check_file(py_file)
        for line_num, message in errors:
            all_errors.append((str(py_file), line_num, message))

    if all_errors:
        print("Linting failed:\n")
        # Sort by file path, then line number
        all_errors.sort(key=lambda x: (x[0], x[1]))
        for file_path, line_num, message in all_errors:
            print(f"{file_path}:{line_num}: {message}")
        return 1

    print("Linting passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
