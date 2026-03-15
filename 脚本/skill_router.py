from __future__ import annotations

import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import 语义路由 as router


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    text = " ".join(sys.argv[1:]).strip()
    print(json.dumps(router.select_skill(text).__dict__, ensure_ascii=False, indent=2))
