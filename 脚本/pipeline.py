"""
Obsidian 笔记处理 Pipeline
核心流程控制器：扫描 → 摘要 → 标签 → 分类 → 路由 → 移动
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# 导入各模块
from 脚本.读写笔记 import 读取笔记, 写入笔记
from 脚本.生成摘要 import 生成摘要
from 脚本.生成标签 import 生成标签
from 脚本.分类笔记 import 分类笔记
from 脚本.语义路由 import 语义路由
from 脚本.安全检查 import 安全检查
from 脚本.移动笔记 import 移动笔记

# Vault 配置
VAULT_PATH = Path("D:/Docs/Notes/ObsidianVault")
INBOX_PATH = VAULT_PATH / "00-收集箱"
QUEUE_FILE = VAULT_PATH / "系统" / "处理队列.json"


class Pipeline:
    """笔记处理流水线"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.queue = self._load_queue()

    def _load_queue(self) -> dict:
        """加载队列"""
        if QUEUE_FILE.exists():
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"queue": [], "processed": [], "failed": [], "last_scan": None}

    def _save_queue(self):
        """保存队列"""
        QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.queue, f, ensure_ascii=False, indent=2)

    def scan(self) -> list:
        """扫描收件箱"""
        notes = []
        if not INBOX_PATH.exists():
            return notes

        for file in INBOX_PATH.glob("*.md"):
            if file.name.startswith("."):
                continue
            # 跳过已在队列中的
            if file.name not in [n["file"] for n in self.queue["queue"]]:
                notes.append({
                    "file": file.name,
                    "path": str(file),
                    "added": datetime.now().isoformat()
                })

        self.queue["queue"].extend(notes)
        self.queue["last_scan"] = datetime.now().isoformat()
        self._save_queue()
        return notes

    def process_next(self) -> Optional[dict]:
        """处理队列中下一条笔记"""
        if not self.queue["queue"]:
            return None

        item = self.queue["queue"].pop(0)
        file_path = Path(item["path"])

        if not file_path.exists():
            self.queue["failed"].append({
                **item,
                "error": "文件不存在",
                "processed_at": datetime.now().isoformat()
            })
            self._save_queue()
            return {"status": "error", "message": "文件不存在"}

        try:
            # 1. 读取笔记内容
            content = 读取笔记(str(file_path))

            # 2. 安全检查
            check_result = 安全检查(content)
            if not check_result["is_safe"]:
                print(f"⚠️ 安全警告: {check_result['issues']}")

            # 3. 生成摘要
            summary_result = 生成摘要(content)
            title = summary_result["title"]
            summary = summary_result["summary"]

            # 4. 生成标签
            tags = 生成标签(content)
            tags.extend(["#待分类", "#自动化处理"])

            # 5. 分类笔记
            category = 分类笔记(content)

            # 6. 语义路由
            routing = 语义路由(content)
            domain = routing["domain"]

            # 构建目标路径
            if category.startswith("20-"):
                target_dir = VAULT_PATH / category / domain
            elif category.startswith("10-"):
                target_dir = VAULT_PATH / category
            elif category.startswith("30-"):
                target_dir = VAULT_PATH / category
            else:
                target_dir = VAULT_PATH / "20-知识库" / domain

            target_dir.mkdir(parents=True, exist_ok=True)

            # 7. 移动笔记
            if self.dry_run:
                result = {
                    "status": "dry_run",
                    "file": item["file"],
                    "title": title,
                    "summary": summary[:100] + "...",
                    "tags": tags,
                    "category": category,
                    "domain": domain,
                    "target_dir": str(target_dir),
                    "target_path": str(target_dir / file_path.name)
                }
                print(f"🔍 [Dry Run] 将处理: {file_path.name}")
                print(f"   标题: {title}")
                print(f"   分类: {category}/{domain}")
                print(f"   标签: {tags}")
                print(f"   目标: {target_dir / file_path.name}")
            else:
                # 更新 frontmatter
                frontmatter = {
                    "title": title,
                    "type": "concept" if category.startswith("20") else "project" if category.startswith("10") else "resource",
                    "domain": [domain],
                    "tags": [t.replace("#", "") for t in tags],
                    "source": "notebooklm",
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "status": "review"
                }
                写入笔记(str(file_path), content, frontmatter)

                # 移动文件
                move_result = 移动笔记(str(file_path), str(target_dir))

                result = {
                    "status": "success",
                    "file": item["file"],
                    "title": title,
                    "category": category,
                    "domain": domain,
                    "target_path": move_result["new_path"],
                    "processed_at": datetime.now().isoformat()
                }

                print(f"✅ 已处理: {file_path.name}")
                print(f"   → {move_result['new_path']}")

            self.queue["processed"].append(result)
            self._save_queue()
            return result

        except Exception as e:
            self.queue["failed"].append({
                **item,
                "error": str(e),
                "processed_at": datetime.now().isoformat()
            })
            self._save_queue()
            return {"status": "error", "message": str(e)}

    def status(self) -> dict:
        """查看队列状态"""
        return {
            "pending": len(self.queue["queue"]),
            "processed": len(self.queue["processed"]),
            "failed": len(self.queue["failed"]),
            "last_scan": self.queue.get("last_scan"),
            "queue": self.queue["queue"]
        }
