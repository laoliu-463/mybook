from __future__ import annotations

import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(pipeline.scan_inbox(), ensure_ascii=False, indent=2))
