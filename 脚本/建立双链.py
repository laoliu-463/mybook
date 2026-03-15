from __future__ import annotations

import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline
import 读写笔记 as note_io


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print(json.dumps({"status": "failed", "error": "需要提供笔记路径"}, ensure_ascii=False, indent=2))
        return 1

    path = note_io.get_vault_root() / sys.argv[1]
    document = note_io.read_note(path)
    tags = note_io.extract_tags(document)
    domains = [str(item) for item in document.frontmatter.get("domain", []) if str(item).strip()]
    links = pipeline.suggest_related_notes(tags=tags, domains=domains, exclude_paths={sys.argv[1]}, limit=5)
    print(json.dumps({"status": "ok", "links": links}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
