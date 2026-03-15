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


MAX_PROCESS_LIMIT = 3

DEFAULT_FEATURE_STATE = [
    {
        "id": "scan-inbox",
        "description": "扫描收件箱并把新笔记写入处理队列",
        "checks": [
            "只扫描 00-收集箱/ 下的 Markdown 文件",
            "重复路径不会重复入队",
            "运行结果落盘到 系统/处理队列.json",
        ],
        "passes": True,
    },
    {
        "id": "summary-basic",
        "description": "为收件箱笔记生成 TL;DR 摘要",
        "checks": [
            "抽取正文高信息段落",
            "写入 TL;DR 正文分区",
            "不删除原始正文",
        ],
        "passes": True,
    },
    {
        "id": "classify-and-move",
        "description": "按 PARA 目录规则分类并移动笔记",
        "checks": [
            "生成目标目录",
            "文件名符合日期前缀规则",
            "不写入受保护目录",
        ],
        "passes": True,
    },
    {
        "id": "route-subagent",
        "description": "基于规则路由到专用子代理",
        "checks": [
            "识别论文类笔记",
            "识别代码片段类笔记",
            "识别会议纪要类笔记",
        ],
        "passes": True,
    },
    {
        "id": "link-and-moc",
        "description": "建立相关双链并增量更新 MOC",
        "checks": [
            "只生成高置信度相关链接",
            "MOC 仅对 20-知识库 笔记更新",
            "不覆盖既有 MOC 内容",
        ],
        "passes": True,
    },
    {
        "id": "hooks-bootstrap",
        "description": "提供 SessionStart/Stop hook 和本地 settings 模板",
        "checks": [
            "存在 .claude/settings.local.json",
            "存在 会话启动hook.py",
            "存在 停止前检查.py",
        ],
        "passes": True,
    },
]


def init_environment() -> dict[str, Any]:
    created: list[str] = []
    normalized: list[str] = []

    system_dir = note_io.get_system_dir()
    system_dir.mkdir(parents=True, exist_ok=True)

    feature_file = note_io.get_feature_list_file()
    if not feature_file.exists():
        save_feature_state(seed_feature_state_from_legacy())
        created.append(note_io.relative_vault_path(feature_file))

    queue_file = note_io.get_queue_file()
    if not queue_file.exists():
        save_queue_state(default_queue_state())
        created.append(note_io.relative_vault_path(queue_file))
    else:
        save_queue_state(load_queue_state())
        normalized.append(note_io.relative_vault_path(queue_file))

    progress_file = note_io.get_progress_file()
    if not progress_file.exists():
        write_progress(load_queue_state(), load_feature_state(), "初始化环境")
        created.append(note_io.relative_vault_path(progress_file))

    run_log_file = note_io.get_run_log_file()
    if not run_log_file.exists():
        run_log_file.write_text("# 运行日志\n\n", encoding="utf-8")
        created.append(note_io.relative_vault_path(run_log_file))

    result = {
        "status": "ok",
        "created": created,
        "normalized": normalized,
        "feature_count": len(load_feature_state()),
        "queue_count": len(load_queue_state()["queue"]),
    }
    append_run_log("init", result)
    write_progress(load_queue_state(), load_feature_state(), "初始化环境", result)
    return result


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
                "steps": {
                    "summary": False,
                    "tags": False,
                    "classified": False,
                    "enhanced": False,
                    "linked": False,
                    "moved": False,
                },
                "summary_generated": False,
                "tags_generated": False,
                "classified": False,
                "skill": None,
                "linked": False,
                "moved": False,
                "applied_agent": None,
                "error": None,
                "created_at": current_timestamp(),
                "updated_at": current_timestamp(),
            }
        )
        added.append(relative_path)

    queue_state["last_scan"] = current_timestamp()
    save_queue_state(queue_state)
    result = {
        "status": "ok",
        "added": added,
        "queue_count": len(queue_state["queue"]),
        "last_scan": queue_state["last_scan"],
    }
    append_run_log("scan", result)
    write_progress(queue_state, load_feature_state(), "扫描收件箱", result)
    return result


def process_batch(*, limit: int = 1, dry_run: bool = False) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, MAX_PROCESS_LIMIT))
    if dry_run:
        preview = process_next(dry_run=True)
        preview["limit"] = bounded_limit
        return preview

    results: list[dict[str, Any]] = []
    for _ in range(bounded_limit):
        result = process_next(dry_run=False)
        results.append(result)
        if result.get("status") in {"empty", "failed"}:
            break

    queue_state = load_queue_state()
    summary = {
        "status": "ok" if not any(item.get("status") == "failed" for item in results) else "failed",
        "processed_count": sum(1 for item in results if item.get("status") == "processed"),
        "results": results,
        "remaining_queue": len(queue_state["queue"]),
    }
    append_run_log("process-batch", summary)
    write_progress(queue_state, load_feature_state(), "批次处理", summary)
    return summary


def process_next(*, dry_run: bool = False) -> dict[str, Any]:
    queue_state = load_queue_state()
    if not queue_state["queue"]:
        return {"status": "empty", "message": "处理队列为空，请先执行 scan。"}

    entry = normalize_queue_entry(queue_state["queue"][0])
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
            "steps": {
                "summary": True,
                "tags": True,
                "classified": True,
                "enhanced": True,
                "linked": bool(related_notes),
                "moved": not dry_run,
            },
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
                "steps": {
                    "summary": True,
                    "tags": True,
                    "classified": True,
                    "enhanced": True,
                    "linked": bool(related_notes),
                    "moved": True,
                },
                "summary_generated": True,
                "tags_generated": True,
                "classified": True,
                "skill": recommended_skill.skill,
                "linked": bool(related_notes),
                "moved": True,
                "applied_agent": recommended_skill.skill,
                "error": None,
                "moc": moc_result,
                "processed_at": current_timestamp(),
            }
        )
        save_queue_state(queue_state)
        preview["moc"] = moc_result
        append_run_log("process-note", preview)
        write_progress(queue_state, load_feature_state(), "处理笔记", preview)
        return preview
    except Exception as exc:
        queue_state["queue"].pop(0)
        failure = {
            "path": entry["path"],
            "status": "failed",
            "steps": entry["steps"],
            "applied_agent": entry.get("applied_agent"),
            "error": str(exc),
            "failed_at": current_timestamp(),
        }
        queue_state["failed"].append(failure)
        save_queue_state(queue_state)
        result = {
            "status": "failed",
            "path": entry["path"],
            "error": str(exc),
        }
        append_run_log("process-note", result)
        write_progress(queue_state, load_feature_state(), "处理失败", result)
        return result


def get_status() -> dict[str, Any]:
    queue_state = load_queue_state()
    feature_state = load_feature_state()
    next_item = queue_state["queue"][0]["path"] if queue_state["queue"] else None
    passed_features = sum(1 for item in feature_state if item.get("passes") is True)
    next_feature = next((item["id"] for item in feature_state if item.get("passes") is False), None)
    return {
        "status": "ok",
        "queue_count": len(queue_state["queue"]),
        "processed_count": len(queue_state["processed"]),
        "failed_count": len(queue_state["failed"]),
        "last_scan": queue_state.get("last_scan"),
        "next_item": next_item,
        "feature_summary": {
            "passed": passed_features,
            "total": len(feature_state),
            "next_feature": next_feature,
        },
    }


def verify_workspace(*, changed_only: bool = False, smoke: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    for label, path in [
        ("功能清单", note_io.get_feature_list_file()),
        ("处理队列", note_io.get_queue_file()),
        ("运行进度", note_io.get_progress_file()),
        ("运行日志", note_io.get_run_log_file()),
        ("frontmatter schema", note_io.get_frontmatter_schema_file()),
        ("process-inbox skill", note_io.get_vault_root() / ".claude" / "skills" / "process-inbox" / "SKILL.md"),
        ("主流程脚本", note_io.get_vault_root() / "脚本" / "主流程.py"),
        ("初始化脚本", note_io.get_vault_root() / "脚本" / "初始化环境.sh"),
    ]:
        checks.append({"name": label, "passed": path.exists(), "detail": note_io.relative_vault_path(path) if path.exists() else f"缺失: {path.name}"})

    feature_state = load_feature_state()
    checks.append(
        {
            "name": "功能清单格式",
            "passed": all(isinstance(item.get("passes"), bool) for item in feature_state),
            "detail": f"{len(feature_state)} 个功能项",
        }
    )

    queue_state = load_queue_state()
    pending_paths = [entry["path"] for entry in queue_state["queue"]]
    checks.append(
        {
            "name": "待处理路径范围",
            "passed": all(path.startswith("00-收集箱/") for path in pending_paths),
            "detail": f"{len(pending_paths)} 条待处理任务",
        }
    )

    if not smoke:
        existing_pending = [
            path for path in pending_paths if (note_io.get_vault_root() / path).exists()
        ]
        checks.append(
            {
                "name": "待处理文件存在",
                "passed": len(existing_pending) == len(pending_paths),
                "detail": f"{len(existing_pending)}/{len(pending_paths)}",
            }
        )
        checks.append(
            {
                "name": "Stop hook 脚本",
                "passed": (note_io.get_vault_root() / "脚本" / "停止前检查.py").exists(),
                "detail": "脚本/停止前检查.py",
            }
        )
        checks.append(
            {
                "name": "SessionStart hook 脚本",
                "passed": (note_io.get_vault_root() / "脚本" / "会话启动hook.py").exists(),
                "detail": "脚本/会话启动hook.py",
            }
        )

    passed = all(item["passed"] for item in checks)
    result = {
        "status": "ok" if passed else "failed",
        "scope": "changed-only" if changed_only else "full",
        "smoke": smoke,
        "checks": checks,
    }
    append_run_log("verify", result)
    return result


def load_queue_state() -> dict[str, Any]:
    queue_file = note_io.get_queue_file()
    if not queue_file.exists():
        return default_queue_state()

    with queue_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return {
        "queue": [normalize_queue_entry(entry) for entry in data.get("queue", [])],
        "processed": [normalize_completed_entry(entry) for entry in data.get("processed", [])],
        "failed": [normalize_failed_entry(entry) for entry in data.get("failed", [])],
        "last_scan": data.get("last_scan"),
    }


def save_queue_state(state: dict[str, Any]) -> None:
    queue_file = note_io.get_queue_file()
    note_io.ensure_parent_dir(queue_file)
    queue_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_feature_state() -> list[dict[str, Any]]:
    feature_file = note_io.get_feature_list_file()
    if not feature_file.exists():
        return seed_feature_state_from_legacy()
    with feature_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return list(data)


def save_feature_state(state: list[dict[str, Any]]) -> None:
    feature_file = note_io.get_feature_list_file()
    note_io.ensure_parent_dir(feature_file)
    feature_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_feature_state_from_legacy() -> list[dict[str, Any]]:
    legacy_file = note_io.get_system_dir() / "feature_list.json"
    if not legacy_file.exists():
        return list(DEFAULT_FEATURE_STATE)

    try:
        with legacy_file.open("r", encoding="utf-8") as file:
            legacy = json.load(file)
    except json.JSONDecodeError:
        return list(DEFAULT_FEATURE_STATE)

    legacy_map = {
        item.get("name"): item.get("status") == "completed"
        for item in legacy.get("features", [])
        if item.get("name")
    }

    state: list[dict[str, Any]] = []
    mapping = {
        "scan-inbox": "scan_inbox",
        "summary-basic": "process_note",
        "classify-and-move": "move_note",
        "route-subagent": "skill_routing",
        "link-and-moc": "generate_moc",
        "hooks-bootstrap": None,
    }
    for feature in DEFAULT_FEATURE_STATE:
        copied = dict(feature)
        legacy_name = mapping.get(feature["id"])
        if legacy_name is not None:
            copied["passes"] = bool(legacy_map.get(legacy_name, feature["passes"]))
        state.append(copied)
    return state


def default_queue_state() -> dict[str, Any]:
    return {
        "queue": [],
        "processed": [],
        "failed": [],
        "last_scan": None,
    }


def normalize_queue_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entry)
    normalized.setdefault("status", "pending")
    normalized.setdefault("steps", {})
    normalized["steps"] = {
        "summary": bool(normalized["steps"].get("summary", normalized.get("summary_generated", False))),
        "tags": bool(normalized["steps"].get("tags", normalized.get("tags_generated", False))),
        "classified": bool(normalized["steps"].get("classified", normalized.get("classified", False))),
        "enhanced": bool(normalized["steps"].get("enhanced", False)),
        "linked": bool(normalized["steps"].get("linked", normalized.get("linked", False))),
        "moved": bool(normalized["steps"].get("moved", normalized.get("moved", False))),
    }
    normalized.setdefault("summary_generated", normalized["steps"]["summary"])
    normalized.setdefault("tags_generated", normalized["steps"]["tags"])
    normalized.setdefault("classified", normalized["steps"]["classified"])
    normalized.setdefault("skill", None)
    normalized.setdefault("linked", normalized["steps"]["linked"])
    normalized.setdefault("moved", normalized["steps"]["moved"])
    normalized.setdefault("applied_agent", normalized.get("skill"))
    normalized.setdefault("error", None)
    normalized.setdefault("created_at", current_timestamp())
    normalized.setdefault("updated_at", current_timestamp())
    return normalized


def normalize_completed_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entry)
    normalized.setdefault(
        "steps",
        {
            "summary": True,
            "tags": True,
            "classified": True,
            "enhanced": True,
            "linked": bool(normalized.get("linked", False)),
            "moved": True,
        },
    )
    normalized.setdefault("applied_agent", normalized.get("skill"))
    normalized.setdefault("error", None)
    return normalized


def normalize_failed_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entry)
    normalized.setdefault(
        "steps",
        {
            "summary": False,
            "tags": False,
            "classified": False,
            "enhanced": False,
            "linked": False,
            "moved": False,
        },
    )
    normalized.setdefault("applied_agent", None)
    normalized.setdefault("error", normalized.get("error"))
    return normalized


def write_progress(
    queue_state: dict[str, Any],
    feature_state: list[dict[str, Any]],
    last_action: str,
    details: dict[str, Any] | None = None,
) -> None:
    progress_file = note_io.get_progress_file()
    passed_count = sum(1 for item in feature_state if item.get("passes") is True)
    next_feature = next((item["id"] for item in feature_state if item.get("passes") is False), "无")
    retry_items = [item["path"] for item in queue_state["failed"][-3:]]
    latest_target = None
    if details:
        latest_target = details.get("destination") or details.get("source")

    lines = [
        "# 运行进度",
        "",
        "## 开发态进度",
        f"- 上次更新：{current_timestamp()}",
        f"- 功能通过：{passed_count}/{len(feature_state)}",
        f"- 下次优先：{next_feature}",
        "",
        "## 运行态进度",
        f"- 上次动作：{last_action}",
        f"- 上次扫描：{queue_state.get('last_scan') or '未扫描'}",
        f"- 待处理：{len(queue_state['queue'])}",
        f"- 已完成：{len(queue_state['processed'])}",
        f"- 失败：{len(queue_state['failed'])}",
        f"- 最近目标：{latest_target or '无'}",
        f"- 待重试：{', '.join(retry_items) if retry_items else '无'}",
        "",
    ]
    progress_file.write_text("\n".join(lines), encoding="utf-8")


def append_run_log(action: str, payload: dict[str, Any]) -> None:
    run_log_file = note_io.get_run_log_file()
    if not run_log_file.exists():
        run_log_file.write_text("# 运行日志\n\n", encoding="utf-8")

    lines = [
        f"## {current_timestamp()} | {action}",
        "",
        "```json",
        json.dumps(payload, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    with run_log_file.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines))


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
