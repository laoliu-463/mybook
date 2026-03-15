from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
from typing import Any

import 分类笔记 as classifier
import 安全检查 as security
import 生成摘要 as summarizer
import 生成标签 as tagger
import 移动笔记 as mover
import 语义路由 as router
import 读写笔记 as note_io


def scan_inbox() -> dict[str, Any]:
    queue_state = load_queue_state()
    inbox_dir = note_io.get_inbox_dir()
    inbox_dir.mkdir(parents=True, exist_ok=True)

    known_paths = {
        entry["path"]
        for bucket in ("queue", "processed", "failed")
        for entry in queue_state.get(bucket, [])
        if entry.get("path")
    }

    added: list[str] = []
    for path in sorted(inbox_dir.rglob("*.md")):
        relative_path = note_io.relative_vault_path(path)
        if relative_path in known_paths:
            continue

        queue_state["queue"].append(
            {
                "path": relative_path,
                "status": "pending",
                "summary_generated": False,
                "tags_generated": False,
                "classified": False,
                "skill": None,
                "linked": False,
                "moved": False,
                "created_at": current_timestamp(),
                "updated_at": current_timestamp(),
            }
        )
        added.append(relative_path)

    queue_state["last_scan"] = current_timestamp()
    save_queue_state(queue_state)
    return {
        "status": "ok",
        "added": added,
        "queue_count": len(queue_state["queue"]),
        "last_scan": queue_state["last_scan"],
    }


def process_next(*, dry_run: bool = False) -> dict[str, Any]:
    queue_state = load_queue_state()
    if not queue_state["queue"]:
        return {"status": "empty", "message": "处理队列为空，请先执行 scan。"}

    entry = queue_state["queue"][0]
    source_path = note_io.get_vault_root() / entry["path"]

    try:
        document = note_io.read_note(source_path)
        full_text = document.path.read_text(encoding="utf-8")
        security.validate_note_for_processing(source_path, full_text)

        title = note_io.extract_title(document)
        classification = classifier.classify_note(title, document.body)
        existing_tags = note_io.extract_tags(document)
        tags = note_io.dedupe_list(existing_tags + tagger.generate_tags(f"{title}\n{document.body}", existing_tags))
        tags = note_io.dedupe_list(tags + classification.domains)
        summary = summarizer.generate_summary(title, document.body)
        recommended_skill = router.select_skill(f"{title}\n{document.body}")
        related_notes = suggest_related_notes(
            tags=tags,
            domains=classification.domains,
            exclude_paths={entry["path"]},
            limit=3,
        )

        created = normalize_created(document.frontmatter.get("created"))
        source = infer_source(document.body, document.frontmatter.get("source"))
        merged_frontmatter = build_frontmatter(
            existing=document.frontmatter,
            title=title,
            note_type=classification.note_type,
            domains=classification.domains,
            tags=tags,
            source=source,
            created=created,
        )
        processed_body = build_processed_body(document.body, title, summary, related_notes)
        destination_path = mover.prepare_destination(classification.target_dir, title, created)
        preview = {
            "status": "preview" if dry_run else "processed",
            "source": entry["path"],
            "destination": note_io.relative_vault_path(destination_path),
            "classification": {
                "target_dir": classification.target_dir,
                "type": classification.note_type,
                "domains": classification.domains,
                "reason": classification.reason,
            },
            "summary": summary,
            "tags": tags,
            "recommended_skill": {
                "name": recommended_skill.skill,
                "score": recommended_skill.score,
                "reason": recommended_skill.reason,
            },
            "related_links": [item["wikilink"] for item in related_notes],
        }

        if dry_run:
            return preview

        rendered = note_io.render_note(merged_frontmatter, processed_body)
        move_result = mover.move_note(source_path, destination_path, rendered)
        moc_result = update_moc(move_result.destination, title, classification.domains)

        queue_state["queue"].pop(0)
        queue_state["processed"].append(
            {
                "path": entry["path"],
                "destination": note_io.relative_vault_path(move_result.destination),
                "status": "done",
                "summary_generated": True,
                "tags_generated": True,
                "classified": True,
                "skill": recommended_skill.skill,
                "linked": bool(related_notes),
                "moved": True,
                "moc": moc_result,
                "processed_at": current_timestamp(),
            }
        )
        save_queue_state(queue_state)
        preview["moc"] = moc_result
        return preview
    except Exception as exc:
        queue_state["queue"].pop(0)
        queue_state["failed"].append(
            {
                "path": entry["path"],
                "status": "failed",
                "error": str(exc),
                "failed_at": current_timestamp(),
            }
        )
        save_queue_state(queue_state)
        return {
            "status": "failed",
            "path": entry["path"],
            "error": str(exc),
        }


def get_status() -> dict[str, Any]:
    queue_state = load_queue_state()
    next_item = queue_state["queue"][0]["path"] if queue_state["queue"] else None
    return {
        "status": "ok",
        "queue_count": len(queue_state["queue"]),
        "processed_count": len(queue_state["processed"]),
        "failed_count": len(queue_state["failed"]),
        "last_scan": queue_state.get("last_scan"),
        "next_item": next_item,
    }


def load_queue_state() -> dict[str, Any]:
    queue_file = note_io.get_queue_file()
    if not queue_file.exists():
        return default_queue_state()
    with queue_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {
        "queue": data.get("queue", []),
        "processed": data.get("processed", []),
        "failed": data.get("failed", []),
        "last_scan": data.get("last_scan"),
    }


def save_queue_state(state: dict[str, Any]) -> None:
    queue_file = note_io.get_queue_file()
    note_io.ensure_parent_dir(queue_file)
    queue_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def default_queue_state() -> dict[str, Any]:
    return {
        "queue": [],
        "processed": [],
        "failed": [],
        "last_scan": None,
    }


def current_timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")


def normalize_created(raw_value: Any) -> str:
    if isinstance(raw_value, str) and raw_value[:10]:
        return raw_value[:10]
    return date.today().isoformat()


def infer_source(body: str, raw_source: Any) -> str:
    if isinstance(raw_source, str) and raw_source in {"notebooklm", "web", "book", "voice"}:
        return raw_source
    lowered = body.lower()
    if "notebooklm" in lowered:
        return "notebooklm"
    if "http://" in lowered or "https://" in lowered:
        return "web"
    return "voice"


def build_frontmatter(
    *,
    existing: dict[str, Any],
    title: str,
    note_type: str,
    domains: list[str],
    tags: list[str],
    source: str,
    created: str,
) -> dict[str, Any]:
    frontmatter = dict(existing)
    allowed_types = {"concept", "overview", "interview", "project", "resource"}
    frontmatter["title"] = title
    frontmatter["type"] = existing.get("type") if existing.get("type") in allowed_types else note_type
    frontmatter["domain"] = domains
    frontmatter["tags"] = tags
    frontmatter["source"] = source
    frontmatter["created"] = created
    frontmatter["status"] = "review"
    return frontmatter


def build_processed_body(
    body: str,
    title: str,
    summary: list[str],
    related_notes: list[dict[str, str]],
) -> str:
    next_body = note_io.ensure_title(body, title)
    summary_block = "\n".join(f"- {item}" for item in summary)
    next_body = note_io.upsert_markdown_section(next_body, "TL;DR", summary_block, insert_after_title=True)

    if related_notes:
        related_block = "\n".join(f"- {item['wikilink']}" for item in related_notes)
        next_body = note_io.upsert_markdown_section(next_body, "相关笔记", related_block)

    if not note_io.has_markdown_section(next_body, "References"):
        next_body = note_io.upsert_markdown_section(next_body, "References", "- 待补充来源或外部引用。")
    if not note_io.has_markdown_section(next_body, "【需要人工复核】"):
        next_body = note_io.upsert_markdown_section(
            next_body,
            "【需要人工复核】",
            "- 自动生成的摘要、标签、分类和相关链接需要人工确认。",
        )
    return next_body


def suggest_related_notes(
    *,
    tags: list[str],
    domains: list[str],
    exclude_paths: set[str],
    limit: int,
) -> list[dict[str, str]]:
    candidates: list[dict[str, Any]] = []
    vault_root = note_io.get_vault_root()
    normalized_tags = {tag.casefold() for tag in tags}
    normalized_domains = {domain.casefold() for domain in domains}

    for path in vault_root.rglob("*.md"):
        relative = note_io.relative_vault_path(path)
        if relative in exclude_paths:
            continue
        if relative.startswith(("00-收集箱/", ".claude/", ".obsidian/", "80-模板/", "99-归档/")):
            continue
        if relative.startswith("20-知识库/MOC-"):
            continue

        try:
            document = note_io.read_note(path)
        except Exception:
            continue

        candidate_tags = {tag.casefold() for tag in note_io.extract_tags(document)}
        candidate_domains = {
            str(item).casefold()
            for item in document.frontmatter.get("domain", [])
            if str(item).strip()
        }
        score = len(normalized_tags & candidate_tags) * 2 + len(normalized_domains & candidate_domains)
        if score <= 0:
            continue

        title = note_io.extract_title(document)
        candidates.append(
            {
                "path": relative,
                "title": title,
                "score": score,
                "wikilink": to_wikilink(relative, title),
            }
        )

    candidates.sort(key=lambda item: (-item["score"], item["path"]))
    return candidates[:limit]


def to_wikilink(relative_path: str, title: str) -> str:
    note_path = relative_path.removesuffix(".md")
    return f"[[{note_path}|{title}]]"


def update_moc(destination: Path, title: str, domains: list[str]) -> dict[str, Any]:
    relative_destination = note_io.relative_vault_path(destination)
    if not relative_destination.startswith("20-知识库/") or not domains:
        return {"updated": False, "reason": "当前笔记不属于 20-知识库，跳过 MOC 更新。"}

    domain = domains[0]
    moc_path = note_io.get_vault_root() / "20-知识库" / f"MOC-{domain}.md"
    security.ensure_safe_write(moc_path)

    if moc_path.exists():
        moc_document = note_io.read_note(moc_path)
    else:
        moc_document = note_io.NoteDocument(
            path=moc_path,
            frontmatter={
                "title": f"MOC-{domain}",
                "type": "overview",
                "domain": [domain],
                "tags": ["MOC", domain],
                "source": "voice",
                "created": date.today().isoformat(),
                "status": "review",
            },
            body=f"# MOC-{domain}\n\n## 索引\n",
        )

    entry = f"- {to_wikilink(relative_destination, title)}"
    if entry not in moc_document.body:
        moc_document.body = note_io.append_to_markdown_section(moc_document.body, "索引", entry)
        note_io.write_note(moc_document)

    return {
        "updated": True,
        "path": note_io.relative_vault_path(moc_path),
    }
