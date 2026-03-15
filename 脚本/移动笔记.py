from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import 安全检查 as security
import 读写笔记 as note_io


@dataclass(frozen=True, slots=True)
class MoveResult:
    destination: Path
    collision_resolved: bool


INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]+')


def build_filename(title: str, created: str) -> str:
    sanitized_title = INVALID_FILENAME_CHARS.sub("-", title).strip().strip(".")
    sanitized_title = re.sub(r"\s+", " ", sanitized_title)
    date_prefix = created[:10]

    if re.match(r"^\d{4}-\d{2}-\d{2}-", sanitized_title):
        return f"{sanitized_title}.md"
    return f"{date_prefix}-{sanitized_title}.md"


def prepare_destination(target_dir: str, title: str, created: str) -> Path:
    vault_root = note_io.get_vault_root()
    destination = vault_root / target_dir / build_filename(title, created)
    security.ensure_safe_write(destination)
    return resolve_collision(destination)


def resolve_collision(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 2
    while True:
        candidate = parent / f"{stem} - {counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def move_note(source: Path, destination: Path, content: str) -> MoveResult:
    security.ensure_safe_read(source)
    security.ensure_safe_write(destination)
    note_io.ensure_parent_dir(destination)
    destination.write_text(content, encoding="utf-8")

    collision_resolved = source.resolve() != destination.resolve() and destination.exists()
    if source.resolve() != destination.resolve():
        source.unlink()

    return MoveResult(destination=destination, collision_resolved=collision_resolved)
