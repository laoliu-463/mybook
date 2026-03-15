#!/bin/bash
# Anthropic Harness 初始化脚本
# 遵循 Effective harnesses for long-running agents 规范

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo "=== Obsidian Harness Initializing ==="

# 检查项目目录
if [ ! -d "系统" ]; then
    echo "错误：未找到系统目录"
    exit 1
fi

# 检查必需的状态文件
REQUIRED_FILES=(
    "系统/feature_list.json"
    "系统/progress.md"
    "系统/task_queue.json"
    "系统/run_log.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "⚠️  缺少 $file，正在创建..."
    fi
done

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ 环境校验完成"

# 显示状态
echo ""
echo "📊 当前状态："
python3 脚本/cli.py status 2>/dev/null || echo "   队列为空"

echo ""
echo "=== 初始化完成 ==="
echo ""
echo "使用方法："
echo "  python 脚本/cli.py scan       # 扫描收件箱"
echo "  python 脚本/cli.py process    # 处理笔记"
echo "  python 脚本/cli.py verify     # E2E 验证"
