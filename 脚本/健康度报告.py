"""
健康度报告生成器

生成系统运行健康度报告。
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from datetime import datetime, timedelta

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline
import 读写笔记 as note_io


def calculate_health_score(
    processed_count: int,
    failed_count: int,
    needs_review_count: int,
    total_runs: int,
) -> float:
    """计算健康度分数 (0-100)"""
    if total_runs == 0:
        return 100.0

    # 基础分数
    score = 100.0

    # 失败率扣分
    failure_rate = (failed_count + needs_review_count) / max(processed_count, 1)
    score -= failure_rate * 50

    # 扣分不能低于 0
    return max(0.0, score)


def generate_health_report() -> dict:
    """生成健康度报告"""
    queue_state = pipeline.load_queue_state()
    feature_state = pipeline.load_feature_state()

    processed = queue_state.get("processed", [])
    failed = queue_state.get("failed", [])
    needs_review = queue_state.get("needs_review", [])

    # 统计
    total_processed = len(processed)
    total_failed = len(failed)
    total_needs_review = len(needs_review)

    # 计算健康度
    health_score = calculate_health_score(
        total_processed,
        total_failed,
        total_needs_review,
        total_processed + total_failed,
    )

    # 失败类型分析
    failure_types = {}
    for item in failed:
        error = item.get("error", "unknown")[:50]
        failure_types[error] = failure_types.get(error, 0) + 1

    # 特征状态
    passed_features = sum(1 for f in feature_state if f.get("passes"))
    total_features = len(feature_state)

    # 计算成功率
    success_rate = (total_processed / max(total_processed + total_failed, 1)) * 100

    return {
        "generated_at": datetime.now().isoformat(),
        "health_score": round(health_score, 1),
        "status": "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical",
        "summary": {
            "total_processed": total_processed,
            "total_failed": total_failed,
            "needs_review": total_needs_review,
            "success_rate": round(success_rate, 1),
        },
        "features": {
            "passed": passed_features,
            "total": total_features,
            "pass_rate": round(passed_features / max(total_features, 1) * 100, 1),
        },
        "failure_analysis": {
            "failure_count": len(failure_types),
            "top_failures": sorted(
                [{"error": k, "count": v} for k, v in failure_types.items()],
                key=lambda x: -x["count"]
            )[:5],
        },
        "recommendations": generate_recommendations(health_score, success_rate, failure_types),
    }


def generate_recommendations(
    health_score: float,
    success_rate: float,
    failure_types: dict,
) -> list[str]:
    """生成建议"""
    recommendations = []

    if health_score < 60:
        recommendations.append("健康度较低，建议检查失败原因并修复系统问题")

    if success_rate < 80:
        recommendations.append(f"成功率 {success_rate:.1f}%，建议分析失败模式")

    if "timeout" in str(failure_types):
        recommendations.append("存在超时错误，建议增加超时时间或优化处理逻辑")

    if "invalid group reference" in str(failure_types):
        recommendations.append("存在正则表达式错误，建议检查代码块格式")

    if not recommendations:
        recommendations.append("系统运行正常")

    return recommendations


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    result = generate_health_report()
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 同时生成 Markdown 报告
    report_path = note_io.get_system_dir() / "健康度报告.md"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"# 系统健康度报告\n\n")
        f.write(f"生成时间: {result['generated_at']}\n\n")
        f.write(f"## 总体评分\n\n")
        f.write(f"- **健康度**: {result['health_score']} / 100 ({result['status']})\n\n")
        f.write(f"## 处理统计\n\n")
        f.write(f"- 成功处理: {result['summary']['total_processed']}\n")
        f.write(f"- 失败: {result['summary']['total_failed']}\n")
        f.write(f"- 待复核: {result['summary']['needs_review']}\n")
        f.write(f"- 成功率: {result['summary']['success_rate']}%\n\n")
        f.write(f"## 功能状态\n\n")
        f.write(f"- 已通过: {result['features']['passed']}/{result['features']['total']}\n")
        f.write(f"- 通过率: {result['features']['pass_rate']}%\n\n")
        f.write(f"## 建议\n\n")
        for rec in result['recommendations']:
            f.write(f"- {rec}\n")

    print(f"\n报告已保存到: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
