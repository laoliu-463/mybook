from __future__ import annotations

from contextlib import contextmanager
from datetime import date, datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import Any

import 分类笔记 as classifier
import 安全检查 as security
import 生成摘要 as summarizer
import 生成标签 as tagger
import 移动笔记 as mover
import 语义路由 as router
import 读写笔记 as note_io
import subagent_router
import 校验frontmatter as frontmatter_validator
import 笔记格式优化 as format_optimizer


MAX_PROCESS_LIMIT = 3
DEFAULT_MAX_RETRIES = 2
ALLOWED_QUEUE_STATUSES = {"pending", "processing", "done", "failed", "needs_review"}
MOC_MANUAL_START = "<!-- MANUAL-START -->"
MOC_MANUAL_END = "<!-- MANUAL-END -->"
MOC_AUTO_START = "<!-- AUTO-START -->"
MOC_AUTO_END = "<!-- AUTO-END -->"

DEFAULT_FEATURE_STATE = [
    {
        "id": "scan-inbox",
        "description": "扫描收件箱并把新笔记写入处理队列",
        "checks": [
            "只扫描 00-收集箱 下的 Markdown 文件",
            "重复路径不会重复入队",
            "结果会落盘到 系统/处理队列.json",
        ],
        "passes": True,
    },
    {
        "id": "summary-basic",
        "description": "为收件箱笔记生成 TL;DR 摘要",
        "checks": [
            "抽取正文高信息密度段落",
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
        "description": "基于规则识别应由哪个子代理接手并生成提示",
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
            "保留人工编辑内容",
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
    {
        "id": "development-session-bootstrap",
        "description": "提供开发态恢复入口并返回下一个未完成能力点",
        "checks": [
            "提供 cli develop 入口",
            "恢复运行进度、功能清单和处理队列摘要",
            "开发态恢复会写回运行进度",
        ],
        "passes": True,
    },
    {
        "id": "git-context-recovery",
        "description": "开发态和会话启动时恢复 git 上下文",
        "checks": [
            "输出当前分支",
            "输出最近一次提交",
            "输出工作区脏文件摘要",
        ],
        "passes": True,
    },
    {
        "id": "subagent-execution",
        "description": "提供 Claude 子代理执行适配层，失败时安全降级到本地增强",
        "checks": [
            "命中子代理后优先尝试 Claude agent",
            "失败时降级为本地结构化增强",
            "执行结果与 fallback 原因写回状态和日志",
        ],
        "passes": True,
    },
    {
        "id": "fixture-e2e-verification",
        "description": "提供固定样例和失败回归样例的端到端验证",
        "checks": [
            "存在最小样例笔记",
            "存在固定回归样例与 expected 文件",
            "断言 frontmatter、目标目录、队列状态和子代理路由",
        ],
        "passes": True,
    },
]


def init_environment(*, record: bool = True) -> dict[str, Any]:
    created: list[str] = []
    normalized: list[str] = []

    system_dir = note_io.get_system_dir()
    system_dir.mkdir(parents=True, exist_ok=True)

    feature_file = note_io.get_feature_list_file()
    if not feature_file.exists():
        save_feature_state(seed_feature_state_from_legacy())
        created.append(note_io.relative_vault_path(feature_file))
    else:
        existing_feature_state = read_feature_state_file(feature_file)
        normalized_feature_state = normalize_feature_state(existing_feature_state)
        if normalized_feature_state != existing_feature_state:
            save_feature_state(normalized_feature_state)
            normalized.append(note_io.relative_vault_path(feature_file))

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

    health_report_file = note_io.get_system_dir() / "健康度报告.md"
    if not health_report_file.exists():
        health_report_file.write_text("# 健康度报告\n\n- 最近运行统计尚未生成。\n", encoding="utf-8")
        created.append(note_io.relative_vault_path(health_report_file))

    result = {
        "status": "ok",
        "created": created,
        "normalized": normalized,
        "feature_count": len(load_feature_state()),
        "queue_count": len(load_queue_state()["queue"]),
    }
    if record:
        append_run_log("init", result)
        write_progress(load_queue_state(), load_feature_state(), "初始化环境", result)
    return result


def scan_inbox(*, dry_run: bool = False) -> dict[str, Any]:
    queue_state = load_queue_state()
    inbox_dir = note_io.get_inbox_dir()
    inbox_dir.mkdir(parents=True, exist_ok=True)

    known_paths = {
        entry["path"]
        for bucket in ("queue", "processed", "failed", "needs_review")
        for entry in queue_state.get(bucket, [])
        if entry.get("path")
    }

    added: list[str] = []
    preview_entries: list[dict[str, Any]] = []
    for path in sorted(inbox_dir.rglob("*.md")):
        relative_path = note_io.relative_vault_path(path)
        if relative_path in known_paths:
            continue
        entry = build_queue_entry(relative_path)
        preview_entries.append(entry)
        added.append(relative_path)
        if not dry_run:
            queue_state["queue"].append(entry)

    queue_state["last_scan"] = current_timestamp()
    result = {
        "status": "ok",
        "added": added,
        "queue_count": len(queue_state["queue"]) if not dry_run else len(queue_state["queue"]) + len(preview_entries),
        "last_scan": queue_state["last_scan"],
        "dry_run": dry_run,
        "preview_entries": preview_entries,
    }
    if not dry_run:
        save_queue_state(queue_state)
        append_run_log("scan", result)
        write_progress(queue_state, load_feature_state(), "扫描收件箱", result)
    return result


def process_batch(*, limit: int = 1, dry_run: bool = False) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, MAX_PROCESS_LIMIT))

    if dry_run:
        queue_state = load_queue_state()
        preview_queue = [normalize_queue_entry(entry) for entry in queue_state["queue"]]
        scan_preview = scan_inbox(dry_run=True)
        preview_queue.extend([normalize_queue_entry(entry) for entry in scan_preview["preview_entries"]])
        results = [build_processing_preview(entry) for entry in preview_queue[:bounded_limit]]
        summary = summarize_batch_results(results, remaining_queue=max(len(preview_queue) - len(results), 0))
        summary["dry_run"] = True
        summary["limit"] = bounded_limit
        summary["scan_preview"] = scan_preview
        return summary

    results: list[dict[str, Any]] = []
    for _ in range(bounded_limit):
        result = process_next(dry_run=False)
        results.append(result)
        if result.get("status") == "empty":
            break

    queue_state = load_queue_state()
    summary = summarize_batch_results(results, remaining_queue=len(queue_state["queue"]))
    summary["dry_run"] = False
    append_run_log("process", summary)
    write_progress(queue_state, load_feature_state(), "批量处理", summary)
    update_health_report()
    return summary


def process_next(*, dry_run: bool = False) -> dict[str, Any]:
    queue_state = load_queue_state()
    entry_index = next(
        (index for index, entry in enumerate(queue_state["queue"]) if entry.get("status") == "pending"),
        None,
    )
    if entry_index is None:
        return {"status": "empty", "message": "处理队列为空，请先执行 scan。"}

    entry = normalize_queue_entry(queue_state["queue"][entry_index])
    if dry_run:
        return build_processing_preview(entry)

    entry["status"] = "processing"
    entry["processing_started_at"] = current_timestamp()
    entry["updated_at"] = current_timestamp()
    queue_state["queue"][entry_index] = entry
    save_queue_state(queue_state)

    try:
        preview, context = prepare_note_processing(entry, dry_run=False)
        move_result = mover.move_note(context["source_path"], context["destination_path"], context["rendered"])
        moc_result = update_moc(move_result.destination, context["title"], context["classification"].domains)

        queue_state = load_queue_state()
        active_index = find_queue_entry_index(queue_state["queue"], entry["path"], {"processing", "pending"})
        if active_index is not None:
            queue_state["queue"].pop(active_index)

        completed_entry = normalize_completed_entry(
            {
                "path": entry["path"],
                "destination": note_io.relative_vault_path(move_result.destination),
                "status": "done",
                "steps": {**context["steps"], "moved": True},
                "summary_generated": True,
                "tags_generated": True,
                "classified": True,
                "skill": context["recommended_skill"].skill,
                "linked": bool(context["related_notes"]),
                "moved": True,
                "applied_agent": context["applied_agent"],
                "subagent_invoked": context["subagent"]["invoked"],
                "subagent_confidence": context["subagent"]["confidence"],
                "subagent_mode": context["subagent"]["mode"],
                "subagent_error": context["subagent"]["error"],
                "fallback_used": context["subagent"]["fallback_used"],
                "fallback_reason": context["subagent"]["fallback_reason"],
                "error": None,
                "moc": moc_result,
                "processed_at": current_timestamp(),
                "updated_at": current_timestamp(),
            }
        )
        queue_state["processed"].append(completed_entry)
        save_queue_state(queue_state)

        return {
            **preview,
            "status": "processed",
            "destination": note_io.relative_vault_path(move_result.destination),
            "will_write": True,
            "moc": moc_result,
        }
    except Exception as exc:
        queue_state = load_queue_state()
        active_index = find_queue_entry_index(queue_state["queue"], entry["path"], {"processing", "pending"})
        if active_index is not None:
            queue_state["queue"].pop(active_index)

        retry_count = int(entry.get("retry_count", 0)) + 1
        max_retries = int(entry.get("max_retries", DEFAULT_MAX_RETRIES))
        failure_reason = subagent_router.classify_fallback_reason(str(exc))
        failure_record = normalize_failed_entry(
            {
                **entry,
                "status": "failed",
                "retry_count": retry_count,
                "max_retries": max_retries,
                "last_failed_at": current_timestamp(),
                "updated_at": current_timestamp(),
                "error": str(exc),
                "fallback_used": True,
                "fallback_reason": failure_reason,
            }
        )
        queue_state["failed"].append(failure_record)

        if retry_count < max_retries:
            queue_state["queue"].append(
                normalize_queue_entry(
                    {
                        **failure_record,
                        "status": "pending",
                        "updated_at": current_timestamp(),
                    }
                )
            )
        else:
            queue_state["needs_review"].append(
                normalize_failed_entry(
                    {
                        **failure_record,
                        "status": "needs_review",
                        "updated_at": current_timestamp(),
                    }
                )
            )

        save_queue_state(queue_state)
        return {
            "status": "failed",
            "path": entry["path"],
            "error": str(exc),
            "retry_count": retry_count,
            "max_retries": max_retries,
            "needs_review": retry_count >= max_retries,
            "fallback_reason": failure_reason,
        }


def get_status() -> dict[str, Any]:
    queue_state = load_queue_state()
    feature_state = load_feature_state()
    next_item = next((entry["path"] for entry in queue_state["queue"] if entry.get("status") == "pending"), None)
    passed_features = sum(1 for item in feature_state if item.get("passes") is True)
    next_feature = next((item["id"] for item in feature_state if item.get("passes") is False), None)
    return {
        "status": "ok",
        "queue_count": len(queue_state["queue"]),
        "processed_count": len(queue_state["processed"]),
        "failed_count": len(queue_state["failed"]),
        "needs_review_count": len(queue_state["needs_review"]),
        "last_scan": queue_state.get("last_scan"),
        "next_item": next_item,
        "feature_summary": {
            "passed": passed_features,
            "total": len(feature_state),
            "next_feature": next_feature,
        },
    }


def prepare_development_cycle(
    *,
    run_verify: bool = True,
    record: bool = True,
) -> dict[str, Any]:
    init_result = init_environment(record=False)
    queue_state = load_queue_state()
    feature_state = load_feature_state()
    next_feature = next((item for item in feature_state if item.get("passes") is False), None)
    git_context = get_git_context()
    verification = verify_workspace(changed_only=True, smoke=True, record=False) if run_verify else None

    result = {
        "status": "ok" if verification is None or verification.get("status") == "ok" else "failed",
        "init": init_result,
        "git": git_context,
        "feature_summary": {
            "passed": sum(1 for item in feature_state if item.get("passes") is True),
            "total": len(feature_state),
            "next_feature": next_feature,
            "pending": [item["id"] for item in feature_state if item.get("passes") is False][:5],
        },
        "runtime_summary": {
            "queue_count": len(queue_state["queue"]),
            "processed_count": len(queue_state["processed"]),
            "failed_count": len(queue_state["failed"]),
            "needs_review_count": len(queue_state["needs_review"]),
            "last_scan": queue_state.get("last_scan"),
        },
        "progress_excerpt": read_progress_excerpt(),
        "verify": verification,
    }
    if record:
        append_run_log("develop", result)
        write_progress(queue_state, feature_state, "开发态恢复", result)
    return result


def run_fixture_e2e_check(*, record: bool = True) -> dict[str, Any]:
    fixture_source = Path(__file__).resolve().parent.parent / "系统" / "测试样例" / "代码片段样例.md"
    if not fixture_source.exists():
        result = {"status": "failed", "error": f"缺少测试样例: {fixture_source.name}"}
        if record:
            append_run_log("e2e", result)
        return result

    result = run_isolated_case(
        case_name="fixture-sample",
        fixture_source=fixture_source,
        expected={
            "expected_type": "concept",
            "expected_target_dir": "20-知识库/编程语言",
            "expected_agent": "process-code-snippet",
            "must_have_frontmatter": ["title", "type", "domain", "tags", "source", "created", "status"],
            "must_have_sections": ["TL;DR", "References", "【需要人工复核】", "示例说明"],
            "must_not_fail": True,
        },
    )
    if record:
        append_run_log("e2e", result)
    return result


def run_e2e_suite(*, include_fixture: bool = True, record: bool = True) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    if include_fixture:
        cases.append(run_fixture_e2e_check(record=False))
    cases.extend(run_regression_suite(record=False)["cases"])

    result = {
        "status": "ok" if all(case.get("status") == "ok" for case in cases) else "failed",
        "cases": cases,
        "case_count": len(cases),
        "passed_count": sum(1 for case in cases if case.get("status") == "ok"),
        "failed_count": sum(1 for case in cases if case.get("status") != "ok"),
    }
    if record:
        append_run_log("e2e", result)
    return result


def run_regression_suite(*, record: bool = True) -> dict[str, Any]:
    regressions_dir = note_io.get_vault_root() / "测试" / "regressions"
    cases: list[dict[str, Any]] = []
    if regressions_dir.exists():
        for fixture_path in sorted(regressions_dir.glob("*.md")):
            expected_path = fixture_path.with_suffix(".expected.json")
            expected = json.loads(expected_path.read_text(encoding="utf-8-sig")) if expected_path.exists() else {}
            cases.append(
                run_isolated_case(
                    case_name=fixture_path.stem,
                    fixture_source=fixture_path,
                    expected=expected,
                )
            )

    result = {
        "status": "ok" if all(case.get("status") == "ok" for case in cases) else "failed",
        "cases": cases,
    }
    if record:
        append_run_log("regression", result)
    return result


def run_isolated_case(
    *,
    case_name: str,
    fixture_source: Path,
    expected: dict[str, Any],
) -> dict[str, Any]:
    sandbox_parent = note_io.get_vault_root() / ".harness-e2e"
    sandbox_parent.mkdir(parents=True, exist_ok=True)
    sandbox_root = sandbox_parent / f"{case_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    if sandbox_root.exists():
        shutil.rmtree(sandbox_root, ignore_errors=True)
    sandbox_root.mkdir(parents=True, exist_ok=True)

    try:
        build_fixture_sandbox(sandbox_root, fixture_source)
        with temporary_vault_root(sandbox_root):
            init_environment(record=False)
            scan_result = scan_inbox(dry_run=False)
            process_result = process_batch(limit=1, dry_run=False)
            queue_state = load_queue_state()
            checks, destination = assert_case_expectations(
                queue_state=queue_state,
                process_result=process_result,
                expected=expected,
            )
            verify_result = verify_isolated_workspace()
            checks.append(
                {
                    "name": "workspace verify",
                    "passed": verify_result.get("status") == "ok",
                    "detail": verify_result.get("status"),
                }
            )
            return {
                "status": "ok" if all(item["passed"] for item in checks) else "failed",
                "case": case_name,
                "scan": scan_result,
                "process": process_result,
                "checks": checks,
                "destination": destination,
            }
    finally:
        shutil.rmtree(sandbox_root, ignore_errors=True)


def verify_workspace(
    *,
    changed_only: bool = False,
    smoke: bool = False,
    record: bool = True,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    required_paths = [
        ("功能清单", note_io.get_feature_list_file()),
        ("处理队列", note_io.get_queue_file()),
        ("运行进度", note_io.get_progress_file()),
        ("运行日志", note_io.get_run_log_file()),
        ("frontmatter schema", note_io.get_frontmatter_schema_file()),
        ("process-inbox skill", note_io.get_vault_root() / ".claude" / "skills" / "process-inbox" / "SKILL.md"),
        ("develop-harness skill", note_io.get_vault_root() / ".claude" / "skills" / "develop-harness" / "SKILL.md"),
        ("主流程脚本", note_io.get_vault_root() / "脚本" / "主流程.py"),
        ("初始化脚本", note_io.get_vault_root() / "脚本" / "初始化环境.sh"),
        ("Windows 初始化脚本", note_io.get_vault_root() / "脚本" / "初始化环境.ps1"),
        ("E2E 验证脚本", note_io.get_vault_root() / "脚本" / "E2E验证.py"),
        ("Frontmatter 校验脚本", note_io.get_vault_root() / "脚本" / "校验frontmatter.py"),
        ("Subagent 执行脚本", note_io.get_vault_root() / "脚本" / "subagent执行.py"),
        ("停止前检查脚本", note_io.get_vault_root() / "脚本" / "停止前检查.py"),
        ("会话启动 hook", note_io.get_vault_root() / "脚本" / "会话启动hook.py"),
        ("fixture sample", note_io.get_vault_root() / "系统" / "测试样例" / "代码片段样例.md"),
        ("regression sample", note_io.get_vault_root() / "测试" / "regressions" / "failed_case_001.md"),
        ("regression expected", note_io.get_vault_root() / "测试" / "regressions" / "failed_case_001.expected.json"),
    ]
    for label, path in required_paths:
        checks.append(
            {
                "name": label,
                "passed": path.exists(),
                "detail": note_io.relative_vault_path(path) if path.exists() else f"missing: {path.name}",
            }
        )

    feature_state = load_feature_state()
    checks.append(
        {
            "name": "功能清单格式",
            "passed": all(isinstance(item.get("passes"), bool) for item in feature_state),
            "detail": f"{len(feature_state)} items",
        }
    )

    queue_state = load_queue_state()
    all_statuses = [
        entry.get("status")
        for bucket in ("queue", "processed", "failed", "needs_review")
        for entry in queue_state.get(bucket, [])
    ]
    checks.append(
        {
            "name": "队列状态值合法",
            "passed": all(status in ALLOWED_QUEUE_STATUSES for status in all_statuses),
            "detail": ",".join(sorted({str(status) for status in all_statuses})) if all_statuses else "empty",
        }
    )
    pending_paths = [entry["path"] for entry in queue_state["queue"]]
    checks.append(
        {
            "name": "待处理路径范围",
            "passed": all(path.startswith("00-收集箱/") for path in pending_paths),
            "detail": f"{len(pending_paths)} pending",
        }
    )

    schema = frontmatter_validator.load_schema()
    checks.append(
        {
            "name": "frontmatter schema 可解析",
            "passed": bool(schema.get("required")),
            "detail": ",".join(schema.get("required", [])),
        }
    )

    git_context = get_git_context()
    checks.append(
        {
            "name": "Git 上下文可恢复",
            "passed": git_context.get("available", False),
            "detail": git_context.get("summary", git_context.get("error", "git unavailable")),
        }
    )

    if not smoke:
        checks.append(
            {
                "name": "运行日志非空",
                "passed": note_io.get_run_log_file().exists() and note_io.get_run_log_file().stat().st_size > 0,
                "detail": note_io.relative_vault_path(note_io.get_run_log_file()),
            }
        )
        checks.append(
            {
                "name": "健康度报告存在",
                "passed": (note_io.get_system_dir() / "健康度报告.md").exists(),
                "detail": "系统/健康度报告.md",
            }
        )

    result = {
        "status": "ok" if all(item["passed"] for item in checks) else "failed",
        "scope": "changed-only" if changed_only else "full",
        "smoke": smoke,
        "checks": checks,
    }
    if record:
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
        "needs_review": [normalize_failed_entry({**entry, "status": "needs_review"}) for entry in data.get("needs_review", [])],
        "last_scan": data.get("last_scan"),
    }


def save_queue_state(state: dict[str, Any]) -> None:
    queue_file = note_io.get_queue_file()
    note_io.ensure_parent_dir(queue_file)
    normalized_state = {
        "queue": [normalize_queue_entry(entry) for entry in state.get("queue", [])],
        "processed": [normalize_completed_entry(entry) for entry in state.get("processed", [])],
        "failed": [normalize_failed_entry(entry) for entry in state.get("failed", [])],
        "needs_review": [normalize_failed_entry({**entry, "status": "needs_review"}) for entry in state.get("needs_review", [])],
        "last_scan": state.get("last_scan"),
    }
    queue_file.write_text(json.dumps(normalized_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_feature_state() -> list[dict[str, Any]]:
    feature_file = note_io.get_feature_list_file()
    if not feature_file.exists():
        return seed_feature_state_from_legacy()
    return normalize_feature_state(read_feature_state_file(feature_file))


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
    mapping = {
        "scan-inbox": "scan_inbox",
        "summary-basic": "process_note",
        "classify-and-move": "move_note",
        "route-subagent": "skill_routing",
        "link-and-moc": "generate_moc",
        "hooks-bootstrap": None,
    }

    state: list[dict[str, Any]] = []
    for feature in DEFAULT_FEATURE_STATE:
        copied = dict(feature)
        legacy_name = mapping.get(feature["id"])
        if legacy_name is not None:
            copied["passes"] = bool(legacy_map.get(legacy_name, feature["passes"]))
        state.append(copied)
    return state


def read_feature_state_file(feature_file: Path) -> list[dict[str, Any]]:
    with feature_file.open("r", encoding="utf-8") as file:
        return list(json.load(file))


def normalize_feature_state(state: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing_by_id = {
        str(item.get("id")): item
        for item in state
        if isinstance(item, dict) and item.get("id")
    }
    normalized: list[dict[str, Any]] = []
    known_ids = {feature["id"] for feature in DEFAULT_FEATURE_STATE}

    for feature in DEFAULT_FEATURE_STATE:
        current = existing_by_id.get(feature["id"], {})
        merged = dict(feature)
        if isinstance(current.get("passes"), bool):
            merged["passes"] = current["passes"]
        normalized.append(merged)

    for item in state:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("id") or "")
        if item_id and item_id not in known_ids:
            normalized.append(item)
    return normalized


def default_queue_state() -> dict[str, Any]:
    return {
        "queue": [],
        "processed": [],
        "failed": [],
        "needs_review": [],
        "last_scan": None,
    }


def normalize_queue_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entry)
    status = str(normalized.get("status") or "pending")
    if status not in ALLOWED_QUEUE_STATUSES:
        status = "pending"

    steps = normalized.get("steps", {})
    normalized["status"] = status
    normalized["steps"] = {
        "summary": bool(steps.get("summary", normalized.get("summary_generated", False))),
        "tags": bool(steps.get("tags", normalized.get("tags_generated", False))),
        "classified": bool(steps.get("classified", normalized.get("classified", False))),
        "enhanced": bool(steps.get("enhanced", False)),
        "linked": bool(steps.get("linked", normalized.get("linked", False))),
        "moved": bool(steps.get("moved", normalized.get("moved", False))),
    }
    normalized.setdefault("summary_generated", normalized["steps"]["summary"])
    normalized.setdefault("tags_generated", normalized["steps"]["tags"])
    normalized.setdefault("classified", normalized["steps"]["classified"])
    normalized.setdefault("skill", None)
    normalized.setdefault("linked", normalized["steps"]["linked"])
    normalized.setdefault("moved", normalized["steps"]["moved"])
    normalized.setdefault("applied_agent", normalized.get("skill"))
    normalized.setdefault("error", None)
    normalized.setdefault("retry_count", 0)
    normalized.setdefault("max_retries", DEFAULT_MAX_RETRIES)
    normalized.setdefault("last_failed_at", None)
    normalized.setdefault("fallback_used", False)
    normalized.setdefault("fallback_reason", None)
    normalized.setdefault("created_at", current_timestamp())
    normalized.setdefault("updated_at", current_timestamp())
    return normalized


def normalize_completed_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_queue_entry({**entry, "status": "done"})
    normalized["steps"] = {
        "summary": True,
        "tags": True,
        "classified": True,
        "enhanced": True,
        "linked": bool(normalized.get("linked", False)),
        "moved": True,
    }
    normalized.setdefault("processed_at", current_timestamp())
    return normalized


def normalize_failed_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_queue_entry(entry)
    if normalized["status"] not in {"failed", "needs_review"}:
        normalized["status"] = "failed"
    normalized.setdefault("last_failed_at", current_timestamp())
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
        latest_target = details.get("destination") or details.get("path") or details.get("source")

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
        f"- 待复核：{len(queue_state['needs_review'])}",
        f"- 最近目标：{latest_target or '无'}",
        f"- 待重试：{', '.join(retry_items) if retry_items else '无'}",
        "",
    ]
    progress_file.write_text("\n".join(lines), encoding="utf-8")


def append_run_log(action: str, payload: dict[str, Any]) -> None:
    run_log_file = note_io.get_run_log_file()
    if not run_log_file.exists():
        run_log_file.write_text("# 运行日志\n\n", encoding="utf-8")
    with run_log_file.open("a", encoding="utf-8") as file:
        file.write("\n".join(render_run_log_section(action, payload)))


def render_run_log_section(action: str, payload: dict[str, Any]) -> list[str]:
    timestamp = current_timestamp().replace("T", " ")
    lines = [f"## {timestamp}", "", f"- 模式：{payload.get('mode', action)}"]

    if action == "process":
        lines.extend(
            [
                f"- 处理数量：{len(payload.get('results', []))}",
                f"- 成功：{payload.get('processed_count', 0)}",
                f"- 失败：{payload.get('failed_count', 0)}",
            ]
        )
        subagent_usage = payload.get("subagent_usage", {})
        if subagent_usage:
            lines.append("- 调用 subagents：")
            for agent_name, count in sorted(subagent_usage.items()):
                lines.append(f"  - {agent_name}: {count}")
        else:
            lines.append("- 调用 subagents：无")
        lines.append(f"- 新增双链：{payload.get('new_links', 0)}")
        lines.append(f"- 更新主题地图：{payload.get('updated_moc_count', 0)}")
        failures = payload.get("failures", [])
        if failures:
            lines.append("- 失败项：")
            for item in failures:
                lines.append(f"  - {item.get('path')} -> {item.get('error')}")
        else:
            lines.append("- 失败项：无")
    elif action == "scan":
        lines.extend(
            [
                f"- 新增入队：{len(payload.get('added', []))}",
                f"- 队列长度：{payload.get('queue_count', 0)}",
                f"- Dry Run：{payload.get('dry_run', False)}",
            ]
        )
    elif action == "e2e":
        lines.extend(
            [
                f"- 样例数：{payload.get('case_count', 1)}",
                f"- 通过：{payload.get('passed_count', 1 if payload.get('status') == 'ok' else 0)}",
                f"- 失败：{payload.get('failed_count', 0 if payload.get('status') == 'ok' else 1)}",
                f"- 状态：{payload.get('status')}",
            ]
        )
    else:
        lines.append(f"- 状态：{payload.get('status', 'ok')}")

    lines.extend(["", ""])
    return lines


def update_health_report() -> None:
    run_log_file = note_io.get_run_log_file()
    health_report_file = note_io.get_system_dir() / "健康度报告.md"
    if not run_log_file.exists():
        return

    content = run_log_file.read_text(encoding="utf-8")
    recent_runs = [chunk for chunk in content.split("## ") if "- 模式：process" in chunk][-20:]
    if not recent_runs:
        health_report_file.write_text("# 健康度报告\n\n- 最近运行统计尚未生成。\n", encoding="utf-8")
        return

    success_count = 0
    total_processed = 0
    total_failed = 0
    for chunk in recent_runs:
        if "\n- 失败：0" in chunk:
            success_count += 1
        total_processed += extract_numeric_metric(chunk, "成功")
        total_failed += extract_numeric_metric(chunk, "失败")

    lines = [
        "# 健康度报告",
        "",
        f"- 最近 {len(recent_runs)} 次运行成功率：{round(success_count / len(recent_runs) * 100, 1)}%",
        f"- 平均每轮处理数量：{round(total_processed / len(recent_runs), 2)}",
        f"- 平均每轮失败数量：{round(total_failed / len(recent_runs), 2)}",
        "",
    ]
    health_report_file.write_text("\n".join(lines), encoding="utf-8")


@contextmanager
def temporary_vault_root(root: Path):
    previous = os.environ.get("OBSIDIAN_VAULT_ROOT")
    os.environ["OBSIDIAN_VAULT_ROOT"] = str(root)
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("OBSIDIAN_VAULT_ROOT", None)
        else:
            os.environ["OBSIDIAN_VAULT_ROOT"] = previous


def build_fixture_sandbox(sandbox_root: Path, fixture_source: Path) -> None:
    for directory in [
        "00-收集箱",
        "10-项目",
        "20-知识库",
        "30-资源",
        "40-交付物",
        "80-模板",
        "99-归档",
        "系统",
        "测试/regressions",
    ]:
        (sandbox_root / directory).mkdir(parents=True, exist_ok=True)

    fixture_destination = sandbox_root / "00-收集箱" / fixture_source.name
    fixture_destination.write_text(fixture_source.read_text(encoding="utf-8"), encoding="utf-8")

    agent_source = Path(__file__).resolve().parent.parent / ".claude" / "agents"
    agent_destination = sandbox_root / ".claude" / "agents"
    agent_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(agent_source, agent_destination, dirs_exist_ok=True)

    schema_source = Path(__file__).resolve().parent.parent / "系统" / "frontmatter_schema.yaml"
    if schema_source.exists():
        shutil.copy2(schema_source, sandbox_root / "系统" / "frontmatter_schema.yaml")

    regressions_source = Path(__file__).resolve().parent.parent / "测试" / "regressions"
    regressions_destination = sandbox_root / "测试" / "regressions"
    if regressions_source.exists():
        shutil.copytree(regressions_source, regressions_destination, dirs_exist_ok=True)


def verify_isolated_workspace() -> dict[str, Any]:
    checks = [
        {"name": "queue file", "passed": note_io.get_queue_file().exists()},
        {"name": "run log", "passed": note_io.get_run_log_file().exists()},
        {"name": "progress file", "passed": note_io.get_progress_file().exists()},
        {"name": "schema", "passed": note_io.get_frontmatter_schema_file().exists()},
    ]
    return {
        "status": "ok" if all(item["passed"] for item in checks) else "failed",
        "checks": checks,
    }


def assert_fixture_e2e(
    queue_state: dict[str, Any],
    process_result: dict[str, Any],
) -> tuple[list[dict[str, Any]], str]:
    return assert_case_expectations(
        queue_state=queue_state,
        process_result=process_result,
        expected={
            "expected_type": "concept",
            "expected_target_dir": "20-知识库/编程语言",
            "expected_agent": "process-code-snippet",
            "must_have_frontmatter": ["title", "type", "domain", "tags", "source", "created", "status"],
            "must_have_sections": ["TL;DR", "References", "【需要人工复核】", "示例说明"],
            "must_not_fail": True,
        },
    )


def assert_case_expectations(
    *,
    queue_state: dict[str, Any],
    process_result: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[list[dict[str, Any]], str]:
    results = process_result.get("results", [])
    process_item = results[0] if results else {}
    destination = str(process_item.get("destination", ""))
    checks: list[dict[str, Any]] = [
        {
            "name": "case processed",
            "passed": process_item.get("status") == "processed",
            "detail": process_item.get("status", "missing"),
        },
        {
            "name": "queue drained",
            "passed": len(queue_state["queue"]) == 0 and len(queue_state["needs_review"]) == 0,
            "detail": f"queue={len(queue_state['queue'])}, review={len(queue_state['needs_review'])}",
        },
    ]

    if expected.get("must_not_fail"):
        checks.append(
            {
                "name": "must not fail",
                "passed": process_result.get("failed_count", 0) == 0 and len(queue_state["failed"]) == 0,
                "detail": str(process_result.get("failed_count", 0)),
            }
        )

    if destination:
        destination_path = note_io.get_vault_root() / destination
        if destination_path.exists():
            document = note_io.read_note(destination_path)
            validation_errors = frontmatter_validator.validate_document(document)
            checks.extend(
                [
                    {"name": "destination exists", "passed": True, "detail": destination},
                    {
                        "name": "expected target dir",
                        "passed": destination.startswith(str(expected.get("expected_target_dir", ""))),
                        "detail": destination,
                    },
                    {
                        "name": "expected type",
                        "passed": document.frontmatter.get("type") == expected.get("expected_type"),
                        "detail": str(document.frontmatter.get("type")),
                    },
                    {
                        "name": "expected agent",
                        "passed": process_item.get("subagent", {}).get("agent") == expected.get("expected_agent"),
                        "detail": str(process_item.get("subagent", {}).get("agent")),
                    },
                    {
                        "name": "required frontmatter",
                        "passed": all(key in document.frontmatter for key in expected.get("must_have_frontmatter", [])),
                        "detail": ",".join(document.frontmatter.keys()),
                    },
                    {
                        "name": "required sections",
                        "passed": all(
                            note_io.has_markdown_section(document.body, heading)
                            for heading in expected.get("must_have_sections", [])
                        ),
                        "detail": ",".join(expected.get("must_have_sections", [])),
                    },
                    {
                        "name": "frontmatter validator",
                        "passed": not validation_errors,
                        "detail": "; ".join(validation_errors) if validation_errors else "ok",
                    },
                ]
            )
        else:
            checks.append({"name": "destination exists", "passed": False, "detail": destination})
    else:
        checks.append({"name": "destination exists", "passed": False, "detail": "missing"})

    return checks, destination


def read_progress_excerpt(max_lines: int = 12) -> str:
    progress_file = note_io.get_progress_file()
    if not progress_file.exists():
        return ""
    return "\n".join(progress_file.read_text(encoding="utf-8").splitlines()[:max_lines])


def get_git_context(max_files: int = 10) -> dict[str, Any]:
    inside_work_tree = run_git_command(["rev-parse", "--is-inside-work-tree"])
    if inside_work_tree != "true":
        return {"available": False, "summary": "当前目录不是 git 工作区", "error": "not-a-git-repo"}

    branch = run_git_command(["branch", "--show-current"]) or "HEAD"
    last_commit = run_git_command(["log", "-1", "--pretty=format:%h %ad %s", "--date=short"]) or "unknown"
    status_output = run_git_command(["status", "--short"]) or ""
    dirty_files = [line.strip() for line in status_output.splitlines() if line.strip()]
    return {
        "available": True,
        "branch": branch,
        "last_commit": last_commit,
        "dirty_count": len(dirty_files),
        "dirty_files": dirty_files[:max_files],
        "summary": f"{branch} | {last_commit} | dirty={len(dirty_files)}",
    }


def run_git_command(args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=note_io.get_vault_root(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None

    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


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
    summary: list[str],
    skill: str | None,
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
    frontmatter["summary"] = " ".join(summary[:2]).strip()
    if skill:
        frontmatter["skill"] = skill
    frontmatter["processed_at"] = current_timestamp()
    return frontmatter


def build_processed_body(
    body: str,
    title: str,
    summary: list[str],
    related_notes: list[dict[str, str]],
    *,
    enhancement_sections: list[dict[str, str]] | None = None,
    review_notes: list[str] | None = None,
) -> str:
    next_body = note_io.ensure_title(body, title)
    summary_block = "\n".join(f"- {item}" for item in summary)
    next_body = note_io.upsert_markdown_section(next_body, "TL;DR", summary_block, insert_after_title=True)

    if related_notes:
        related_block = "\n".join(f"- {item['wikilink']}" for item in related_notes)
        next_body = note_io.upsert_markdown_section(next_body, "相关笔记", related_block)

    format_result = format_optimizer.optimize_note_format(next_body)
    next_body = format_result.optimized_body

    if not note_io.has_markdown_section(next_body, "References"):
        next_body = note_io.upsert_markdown_section(next_body, "References", "- 待补充来源或外部引用")

    for section in enhancement_sections or []:
        heading = section.get("heading", "").strip()
        content = section.get("content", "").strip()
        if heading and content:
            next_body = note_io.upsert_markdown_section(next_body, heading, content)

    review_lines = ["- 自动生成的摘要、标签、分类和相关链接需要人工确认。"]
    for item in review_notes or []:
        text = str(item).strip()
        if text:
            review_lines.append(f"- {text}")
    next_body = note_io.upsert_markdown_section(next_body, "【需要人工复核】", "\n".join(review_lines))
    return next_body


def merge_subagent_classification(
    classification: classifier.ClassificationResult,
    subagent_execution: subagent_router.SubagentExecutionResult,
) -> classifier.ClassificationResult:
    merged_domains = note_io.dedupe_list(classification.domains + subagent_execution.domains)
    return classifier.ClassificationResult(
        target_dir=classification.target_dir,
        note_type=subagent_execution.note_type or classification.note_type,
        domains=merged_domains or classification.domains,
        reason=classification.reason,
    )


def merge_subagent_summary(
    summary: list[str],
    subagent_execution: subagent_router.SubagentExecutionResult,
) -> list[str]:
    if not subagent_execution.sections:
        return summary
    return note_io.dedupe_list([subagent_execution.sections[0].content, *summary])[:3]


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
    return f"[[{relative_path.removesuffix('.md')}|{title}]]"


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
            body=build_default_moc_body(domain),
        )

    entry = f"- {to_wikilink(relative_destination, title)}"
    updated_body, inserted = upsert_moc_auto_entry(moc_document.body, domain, entry)
    if inserted:
        moc_document.body = updated_body
        note_io.write_note(moc_document)

    return {
        "updated": inserted,
        "path": note_io.relative_vault_path(moc_path),
    }


def build_queue_entry(path: str, *, status: str = "pending") -> dict[str, Any]:
    return normalize_queue_entry(
        {
            "path": path,
            "status": status,
            "steps": {
                "summary": False,
                "tags": False,
                "classified": False,
                "enhanced": False,
                "linked": False,
                "moved": False,
            },
            "applied_agent": None,
            "error": None,
            "retry_count": 0,
            "max_retries": DEFAULT_MAX_RETRIES,
            "last_failed_at": None,
            "fallback_used": False,
            "fallback_reason": None,
            "created_at": current_timestamp(),
            "updated_at": current_timestamp(),
        }
    )


def build_processing_preview(entry: dict[str, Any]) -> dict[str, Any]:
    preview, _ = prepare_note_processing(entry, dry_run=True)
    return preview


def prepare_note_processing(entry: dict[str, Any], *, dry_run: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    source_path = note_io.get_vault_root() / entry["path"]
    document = note_io.read_note(source_path)
    full_text = source_path.read_text(encoding="utf-8")
    security.validate_note_for_processing(source_path, full_text)

    title = note_io.extract_title(document)
    classification = classifier.classify_note(title, document.body)
    existing_tags = note_io.extract_tags(document)
    tags = note_io.dedupe_list(existing_tags + tagger.generate_tags(f"{title}\n{document.body}", existing_tags))
    tags = note_io.dedupe_list(tags + classification.domains)
    summary = summarizer.generate_summary(title, document.body)
    recommended_skill = router.select_skill(f"{title}\n{document.body}")

    steps = {
        "summary": True,
        "tags": True,
        "classified": True,
        "enhanced": False,
        "linked": False,
        "moved": False,
    }

    subagent_route = subagent_router.route_to_subagent(f"{title}\n{document.body}")
    subagent_result = {
        "agent": None,
        "invoked": False,
        "confidence": 0.0,
        "reason": None,
        "mode": "none",
        "error": None,
        "tags": [],
        "domains": [],
        "note_type": None,
        "sections": [],
        "review_notes": [],
        "fallback_used": False,
        "fallback_reason": None,
    }
    if subagent_route and subagent_router.should_invoke_subagent(subagent_route, threshold=0.15):
        steps["enhanced"] = True
        subagent_execution = (
            None
            if dry_run
            else subagent_router.execute_subagent(
                subagent_route.agent,
                title=title,
                body=document.body,
            )
        )
        subagent_result = {
            "agent": subagent_route.agent,
            "invoked": not dry_run,
            "confidence": subagent_route.confidence,
            "reason": subagent_route.reason,
            "mode": "planned" if dry_run else subagent_execution.mode,
            "error": None if dry_run else subagent_execution.error,
            "tags": [] if dry_run else subagent_execution.tags,
            "domains": [] if dry_run else subagent_execution.domains,
            "note_type": None if dry_run else subagent_execution.note_type,
            "sections": [] if dry_run else [
                {"heading": section.heading, "content": section.content}
                for section in subagent_execution.sections
            ],
            "review_notes": [] if dry_run else subagent_execution.review_notes,
            "fallback_used": False if dry_run else subagent_execution.fallback_used,
            "fallback_reason": None if dry_run else subagent_execution.fallback_reason,
        }
        if not dry_run:
            tags = note_io.dedupe_list(tags + subagent_execution.tags)
            classification = merge_subagent_classification(classification, subagent_execution)
            summary = merge_subagent_summary(summary, subagent_execution)

    related_notes = suggest_related_notes(
        tags=tags,
        domains=classification.domains,
        exclude_paths={entry["path"]},
        limit=3,
    )
    steps["linked"] = bool(related_notes)

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
        summary=summary,
        skill=subagent_result["agent"] or recommended_skill.skill,
    )
    processed_body = build_processed_body(
        document.body,
        title,
        summary,
        related_notes,
        enhancement_sections=subagent_result["sections"],
        review_notes=subagent_result["review_notes"],
    )
    destination_path = mover.prepare_destination(classification.target_dir, title, created)
    rendered_document = note_io.NoteDocument(
        path=destination_path,
        frontmatter=merged_frontmatter,
        body=processed_body,
    )
    validation_errors = frontmatter_validator.validate_document(rendered_document)
    if validation_errors:
        raise ValueError("; ".join(validation_errors))

    preview = {
        "status": "preview" if dry_run else "ready",
        "path": entry["path"],
        "source": entry["path"],
        "destination": note_io.relative_vault_path(destination_path),
        "predicted_type": classification.note_type,
        "predicted_agent": subagent_result["agent"],
        "predicted_target": classification.target_dir,
        "will_write": not dry_run,
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
        "subagent": {
            "agent": subagent_result["agent"],
            "invoked": subagent_result["invoked"],
            "confidence": subagent_result["confidence"],
            "reason": subagent_result["reason"],
            "mode": subagent_result["mode"],
            "error": subagent_result["error"],
            "fallback_used": subagent_result["fallback_used"],
            "fallback_reason": subagent_result["fallback_reason"],
            "sections": [item["heading"] for item in subagent_result["sections"]],
        },
        "related_links": [item["wikilink"] for item in related_notes],
        "steps": steps,
        "validation_errors": validation_errors,
    }
    return preview, {
        "source_path": source_path,
        "destination_path": destination_path,
        "rendered": note_io.render_note(merged_frontmatter, processed_body),
        "classification": classification,
        "recommended_skill": recommended_skill,
        "related_notes": related_notes,
        "steps": steps,
        "title": title,
        "subagent": subagent_result,
        "applied_agent": subagent_result["agent"] or recommended_skill.skill,
    }


def summarize_batch_results(results: list[dict[str, Any]], *, remaining_queue: int) -> dict[str, Any]:
    success_count = sum(1 for item in results if item.get("status") == "processed")
    preview_count = sum(1 for item in results if item.get("status") == "preview")
    failed_items = [item for item in results if item.get("status") == "failed"]
    subagent_usage: dict[str, int] = {}
    for item in results:
        agent_name = item.get("predicted_agent") or item.get("subagent", {}).get("agent")
        if not agent_name:
            continue
        subagent_usage[agent_name] = subagent_usage.get(agent_name, 0) + 1
    return {
        "status": "failed" if failed_items else "ok",
        "processed_count": success_count,
        "preview_count": preview_count,
        "failed_count": len(failed_items),
        "results": results,
        "remaining_queue": remaining_queue,
        "subagent_usage": subagent_usage,
        "new_links": sum(len(item.get("related_links", [])) for item in results),
        "updated_moc_count": sum(
            1
            for item in results
            if isinstance(item.get("moc"), dict) and item.get("moc", {}).get("updated") is True
        ),
        "failures": [{"path": item.get("path") or item.get("source"), "error": item.get("error")} for item in failed_items],
    }


def find_queue_entry_index(entries: list[dict[str, Any]], path: str, statuses: set[str]) -> int | None:
    for index, entry in enumerate(entries):
        if entry.get("path") == path and entry.get("status") in statuses:
            return index
    return None


def build_default_moc_body(domain: str) -> str:
    return "\n".join(
        [
            f"# MOC-{domain}",
            "",
            "## 人工笔记",
            MOC_MANUAL_START,
            MOC_MANUAL_END,
            "",
            "## 自动生成",
            MOC_AUTO_START,
            MOC_AUTO_END,
        ]
    )


def upsert_moc_auto_entry(body: str, domain: str, entry: str) -> tuple[str, bool]:
    next_body = note_io.ensure_title(body, f"MOC-{domain}")
    next_body = ensure_moc_marker_section(next_body, "人工笔记", MOC_MANUAL_START, MOC_MANUAL_END)
    next_body = ensure_moc_marker_section(next_body, "自动生成", MOC_AUTO_START, MOC_AUTO_END)

    auto_start_index = next_body.find(MOC_AUTO_START)
    auto_end_index = next_body.find(MOC_AUTO_END)
    if auto_start_index == -1 or auto_end_index == -1 or auto_end_index < auto_start_index:
        return next_body, False

    start = auto_start_index + len(MOC_AUTO_START)
    current_lines = [
        line.strip()
        for line in next_body[start:auto_end_index].strip().splitlines()
        if line.strip()
    ]
    if entry in current_lines:
        return next_body, False

    current_lines.append(entry)
    current_lines = sorted(dict.fromkeys(current_lines))
    replacement = MOC_AUTO_START
    replacement += "\n" + "\n".join(current_lines) + "\n" if current_lines else "\n"
    replacement += MOC_AUTO_END
    updated = next_body[:auto_start_index] + replacement + next_body[auto_end_index + len(MOC_AUTO_END):]
    return updated, True


def ensure_moc_marker_section(body: str, heading: str, start_marker: str, end_marker: str) -> str:
    if start_marker in body and end_marker in body:
        return body
    return note_io.upsert_markdown_section(body, heading, f"{start_marker}\n{end_marker}")


def extract_numeric_metric(chunk: str, label: str) -> int:
    prefix = f"- {label}："
    for line in chunk.splitlines():
        if line.startswith(prefix):
            value = line.removeprefix(prefix).strip()
            try:
                return int(value)
            except ValueError:
                return 0
    return 0
