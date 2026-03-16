from __future__ import annotations

import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import subagent_router
import 读写笔记 as note_io


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    if len(sys.argv) < 3:
        print(json.dumps({"status": "failed", "error": "需要提供 agent 名称和笔记路径"}, ensure_ascii=False, indent=2))
        return 1

    agent_name = sys.argv[1]
    path = note_io.get_vault_root() / sys.argv[2]
    document = note_io.read_note(path)
    title = note_io.extract_title(document)
    result = subagent_router.execute_subagent(agent_name, title=title, body=document.body)
    payload = {
        "status": "ok",
        "agent": result.agent,
        "mode": result.mode,
        "fallback_used": result.fallback_used,
        "fallback_reason": result.fallback_reason,
        "note_type": result.note_type,
        "tags": result.tags,
        "domains": result.domains,
        "sections": [{"heading": item.heading, "content": item.content} for item in result.sections],
        "review_notes": result.review_notes,
        "error": result.error,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
