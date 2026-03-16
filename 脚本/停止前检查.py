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

    verification = pipeline.verify_workspace(changed_only=True, smoke=True, record=False)
    progress_file = note_io.get_progress_file()
    run_log_file = note_io.get_run_log_file()
    progress_updated = progress_file.exists() and progress_file.stat().st_size > 0
    run_log_updated = run_log_file.exists() and run_log_file.stat().st_size > 0
    result = {
        "status": "ok" if verification.get("status") == "ok" and progress_updated and run_log_updated else "failed",
        "verify": verification,
        "progress_updated": progress_updated,
        "run_log_updated": run_log_updated,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
