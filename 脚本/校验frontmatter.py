from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import 读写笔记 as note_io


def load_schema() -> dict[str, Any]:
    schema_path = note_io.get_frontmatter_schema_file()
    lines = schema_path.read_text(encoding="utf-8").splitlines()
    schema: dict[str, Any] = {
        "required": [],
        "optional": [],
        "enum": {},
        "required_sections": [],
    }
    mode: str | None = None
    current_enum: str | None = None

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if not line.startswith(" "):
            current_enum = None
            key = stripped.removesuffix(":")
            if key in {"required", "optional", "required_sections"}:
                mode = key
                continue
            if key == "enum":
                mode = "enum"
                continue

        if mode in {"required", "optional", "required_sections"} and stripped.startswith("- "):
            schema[mode].append(stripped[2:].strip())
            continue

        if mode == "enum" and stripped.endswith(":") and not stripped.startswith("- "):
            current_enum = stripped.removesuffix(":")
            schema["enum"][current_enum] = []
            continue

        if mode == "enum" and current_enum and stripped.startswith("- "):
            schema["enum"][current_enum].append(stripped[2:].strip())

    return schema


def validate_frontmatter(frontmatter: dict[str, Any]) -> list[str]:
    schema = load_schema()
    errors: list[str] = []

    for field in schema["required"]:
        value = frontmatter.get(field)
        if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
            errors.append(f"缺少必填字段: {field}")

    for field, allowed in schema["enum"].items():
        if field not in frontmatter or not allowed:
            continue
        value = frontmatter[field]
        if isinstance(value, list):
            if not all(str(item) in allowed for item in value):
                errors.append(f"字段 {field} 包含非法值: {value}")
        elif str(value) not in allowed:
            errors.append(f"字段 {field} 的值不合法: {value}")

    tags = frontmatter.get("tags")
    if tags is not None and not isinstance(tags, list):
        errors.append("字段 tags 必须是数组")

    domains = frontmatter.get("domain")
    if domains is not None and not isinstance(domains, list):
        errors.append("字段 domain 必须是数组")

    return errors


def validate_document(document: note_io.NoteDocument) -> list[str]:
    errors = validate_frontmatter(document.frontmatter)
    schema = load_schema()
    for heading in schema.get("required_sections", []):
        if not note_io.has_markdown_section(document.body, heading):
            errors.append(f"缺少必需分区: {heading}")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print(json.dumps({"status": "failed", "error": "需要提供笔记路径"}, ensure_ascii=False, indent=2))
        return 1

    path = note_io.get_vault_root() / sys.argv[1]
    document = note_io.read_note(path)
    errors = validate_document(document)
    result = {
        "status": "ok" if not errors else "failed",
        "path": note_io.relative_vault_path(path),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
