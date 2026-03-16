from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import 读写笔记 as note_io

AUTOMATION_REQUIRED_SECTIONS = {"TL;DR", "References", "【需要人工复核】"}
TECHNICAL_NOTE_REQUIRED_SECTIONS = {"一句话结论", "标准回答", "为什么", "易错点", "参考来源"}
TECHNICAL_NOTE_REQUIRED_FIELDS = {"title", "tags", "type", "domain", "topic", "question", "created", "updated", "status"}


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
    missing_required: list[str] = []
    missing_technical_required: list[str] = []

    for field in schema["required"]:
        value = frontmatter.get(field)
        if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
            missing_required.append(field)

    for field in TECHNICAL_NOTE_REQUIRED_FIELDS:
        value = frontmatter.get(field)
        if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
            missing_technical_required.append(field)

    if missing_required and missing_technical_required:
        errors.extend(f"缺少必填字段: {field}" for field in missing_required)

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
    if domains is not None and not isinstance(domains, (list, str)):
        errors.append("字段 domain 必须是字符串或数组")

    return errors


def validate_document(document: note_io.NoteDocument) -> list[str]:
    errors = validate_frontmatter(document.frontmatter)
    schema = load_schema()
    schema_required_sections = set(schema.get("required_sections", []))
    automation_valid = all(note_io.has_markdown_section(document.body, heading) for heading in schema_required_sections)
    technical_valid = all(
        note_io.has_markdown_section(document.body, heading) for heading in TECHNICAL_NOTE_REQUIRED_SECTIONS
    )
    technical_candidate = any(document.frontmatter.get(field) for field in ("question", "topic"))

    if not automation_valid and not technical_valid:
        expected = (
            sorted(TECHNICAL_NOTE_REQUIRED_SECTIONS)
            if technical_candidate
            else sorted(schema_required_sections or AUTOMATION_REQUIRED_SECTIONS)
        )
        for heading in expected:
            if not note_io.has_markdown_section(document.body, heading):
                errors.append(f"缺少必需分区: {heading}")
        if not technical_candidate and not schema_required_sections:
            for heading in sorted(AUTOMATION_REQUIRED_SECTIONS):
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
