from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


REQUIRED_FRONTMATTER_ORDER = [
    "title",
    "type",
    "domain",
    "tags",
    "source",
    "created",
    "status",
]


@dataclass(slots=True)
class NoteDocument:
    path: Path
    frontmatter: dict[str, Any]
    body: str


def get_vault_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_queue_file() -> Path:
    return get_vault_root() / "系统" / "处理队列.json"


def get_inbox_dir() -> Path:
    return get_vault_root() / "00-收集箱"


def relative_vault_path(path: Path) -> str:
    return path.resolve().relative_to(get_vault_root()).as_posix()


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_note(path: Path) -> NoteDocument:
    raw_text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(raw_text)
    return NoteDocument(path=path, frontmatter=frontmatter, body=body)


def write_note(document: NoteDocument) -> None:
    ensure_parent_dir(document.path)
    document.path.write_text(render_note(document.frontmatter, document.body), encoding="utf-8")


def render_note(frontmatter: dict[str, Any], body: str) -> str:
    cleaned_body = body.strip("\n")
    if not frontmatter:
        return f"{cleaned_body}\n"

    yaml_lines = ["---"]
    for key, value in ordered_frontmatter(frontmatter).items():
        yaml_lines.append(f"{key}: {format_frontmatter_value(value)}")
    yaml_lines.append("---")
    yaml_lines.append("")
    yaml_lines.append(cleaned_body)
    return "\n".join(yaml_lines).rstrip() + "\n"


def ordered_frontmatter(frontmatter: dict[str, Any]) -> dict[str, Any]:
    ordered: dict[str, Any] = {}
    for key in REQUIRED_FRONTMATTER_ORDER:
        if key in frontmatter:
            ordered[key] = frontmatter[key]
    for key, value in frontmatter.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("\ufeff"):
        text = text.removeprefix("\ufeff")

    if not text.startswith("---"):
        return {}, text.strip("\n")

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text.strip("\n")

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, text.strip("\n")

    raw_frontmatter = lines[1:end_index]
    parsed, success = parse_frontmatter_lines(raw_frontmatter)
    if not success or not parsed:
        return {}, text.strip("\n")

    body = "\n".join(lines[end_index + 1 :]).strip("\n")
    return parsed, body


def parse_frontmatter_lines(lines: list[str]) -> tuple[dict[str, Any], bool]:
    frontmatter: dict[str, Any] = {}
    index = 0
    parsed_keys = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            index += 1
            continue

        if ":" not in line:
            return {}, False

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            return {}, False

        if value:
            frontmatter[key] = parse_frontmatter_value(value)
            parsed_keys += 1
            index += 1
            continue

        list_values: list[Any] = []
        probe = index + 1
        while probe < len(lines):
            candidate = lines[probe]
            candidate_stripped = candidate.strip()

            if not candidate_stripped:
                probe += 1
                continue

            if candidate.startswith("  - ") or candidate.startswith("- "):
                item = candidate_stripped.removeprefix("- ").strip()
                list_values.append(parse_frontmatter_value(item))
                probe += 1
                continue

            break

        frontmatter[key] = list_values if list_values else ""
        parsed_keys += 1
        index = probe

    return frontmatter, parsed_keys > 0


def parse_frontmatter_value(value: str) -> Any:
    normalized = value.strip()
    if normalized in {"[]", "[ ]"}:
        return []
    if normalized.startswith("[") and normalized.endswith("]"):
        inner = normalized[1:-1].strip()
        if not inner:
            return []
        return [parse_frontmatter_value(part.strip()) for part in split_inline_list(inner)]
    if normalized in {"true", "false"}:
        return normalized == "true"
    if normalized == "null":
        return None
    if re.fullmatch(r"-?\d+", normalized):
        return int(normalized)
    if (
        (normalized.startswith('"') and normalized.endswith('"'))
        or (normalized.startswith("'") and normalized.endswith("'"))
    ):
        return normalized[1:-1]
    return normalized


def split_inline_list(value: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    quote: str | None = None

    for char in value:
        if char in {'"', "'"}:
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            current.append(char)
            continue

        if char == "," and quote is None:
            items.append("".join(current).strip())
            current = []
            continue

        current.append(char)

    if current:
        items.append("".join(current).strip())
    return items


def format_frontmatter_value(value: Any) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(format_scalar(item) for item in value) + "]"
    return format_scalar(value)


def format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if not isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)

    if not value:
        return '""'

    if re.search(r"[:#\[\]\{\},&*!?|>'\"%@`]", value) or value != value.strip():
        return json.dumps(value, ensure_ascii=False)
    return value


def extract_title(document: NoteDocument) -> str:
    title = document.frontmatter.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()

    heading = re.search(r"(?m)^#\s+(.+?)\s*$", document.body)
    if heading:
        return heading.group(1).strip()

    return document.path.stem


def extract_tags(document: NoteDocument) -> list[str]:
    tags: list[str] = []
    frontmatter_tags = document.frontmatter.get("tags", [])
    if isinstance(frontmatter_tags, str):
        tags.append(frontmatter_tags.lstrip("#"))
    elif isinstance(frontmatter_tags, list):
        tags.extend(str(tag).lstrip("#") for tag in frontmatter_tags if str(tag).strip())

    content_tags = re.findall(r"(?<!\w)#([\w\-/\u4e00-\u9fff]+)", document.body)
    tags.extend(content_tags)
    return dedupe_list(tags)


def dedupe_list(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(normalized)
    return result


def ensure_title(body: str, title: str) -> str:
    trimmed = body.strip("\n")
    if re.search(r"(?m)^#\s+.+$", trimmed):
        return trimmed
    return f"# {title}\n\n{trimmed}".strip("\n")


def upsert_markdown_section(
    body: str,
    heading: str,
    content: str,
    *,
    insert_after_title: bool = False,
) -> str:
    trimmed = body.strip("\n")
    section_block = f"## {heading}\n\n{content.strip()}"
    pattern = re.compile(rf"(?ms)^##\s+{re.escape(heading)}\s*$")
    match = pattern.search(trimmed)

    if match:
        next_heading = re.search(r"(?m)^##\s+.+$", trimmed[match.end() :])
        if next_heading:
            end = match.end() + next_heading.start()
        else:
            end = len(trimmed)
        updated = trimmed[: match.start()].rstrip("\n") + "\n\n" + section_block
        suffix = trimmed[end:].lstrip("\n")
        if suffix:
            updated += "\n\n" + suffix
        return updated.strip("\n")

    if insert_after_title:
        title_match = re.search(r"(?m)^#\s+.+$", trimmed)
        if title_match:
            insert_position = title_match.end()
            prefix = trimmed[:insert_position].rstrip("\n")
            suffix = trimmed[insert_position:].lstrip("\n")
            combined = prefix + "\n\n" + section_block
            if suffix:
                combined += "\n\n" + suffix
            return combined.strip("\n")

    return (trimmed + "\n\n" + section_block).strip("\n")


def has_markdown_section(body: str, heading: str) -> bool:
    trimmed = body.strip("\n")
    return re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", trimmed) is not None


def append_to_markdown_section(body: str, heading: str, item: str) -> str:
    trimmed = body.strip("\n")
    pattern = re.compile(rf"(?ms)^##\s+{re.escape(heading)}\s*$")
    match = pattern.search(trimmed)

    if not match:
        return upsert_markdown_section(trimmed, heading, item)

    next_heading = re.search(r"(?m)^##\s+.+$", trimmed[match.end() :])
    if next_heading:
        end = match.end() + next_heading.start()
    else:
        end = len(trimmed)

    section_content = trimmed[match.end() : end].strip("\n")
    lines = [line for line in section_content.splitlines() if line.strip()]
    if item in lines:
        return trimmed

    lines.append(item)
    merged_content = "\n".join(lines)
    updated = trimmed[: match.start()].rstrip("\n") + "\n\n" + f"## {heading}\n\n{merged_content}"
    suffix = trimmed[end:].lstrip("\n")
    if suffix:
        updated += "\n\n" + suffix
    return updated.strip("\n")
