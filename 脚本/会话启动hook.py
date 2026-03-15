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

    status = pipeline.get_status()
    progress_file = note_io.get_progress_file()
    progress_excerpt = ""
    if progress_file.exists():
        progress_excerpt = "\n".join(progress_file.read_text(encoding="utf-8").splitlines()[:12])

    payload = {
        "status": status,
        "progress_excerpt": progress_excerpt,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
