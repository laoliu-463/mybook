from __future__ import annotations

import re


def generate_summary(title: str, body: str, limit: int = 3) -> list[str]:
    cleaned = clean_markdown(body)
    paragraphs = [paragraph.strip() for paragraph in cleaned.split("\n\n") if paragraph.strip()]

    bullets: list[str] = []
    for paragraph in paragraphs:
        sentence = first_sentence(paragraph)
        if not sentence:
            continue
        if looks_like_heading(sentence):
            continue
        bullets.append(sentence)
        if len(bullets) >= limit:
            break

    if not bullets:
        bullets.append(f"{title} 的核心内容需要人工补充摘要。")

    return [truncate(item) for item in bullets]


def clean_markdown(body: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", body)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"(?m)^\s*[-*_]{3,}\s*$", " ", text)
    text = re.sub(r"(?m)^\s*>+\s?", "", text)
    text = re.sub(r"(?m)^#{1,6}\s+", "", text)
    text = re.sub(r"(?m)^\|.+\|$", " ", text)
    text = re.sub(r"(?m)^[-*]\s+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def first_sentence(paragraph: str) -> str:
    compact = " ".join(paragraph.split())
    if not compact:
        return ""

    match = re.split(r"(?<=[。！？!?；;])\s+", compact, maxsplit=1)
    candidate = match[0].strip()
    if len(candidate) < 12 and len(match) > 1:
        candidate = f"{candidate} {match[1].split('。', 1)[0]}".strip()
    return candidate


def truncate(text: str, max_length: int = 90) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 1].rstrip() + "…"


def looks_like_heading(text: str) -> bool:
    compact = text.strip()
    if re.fullmatch(r"\d+(?:\.\d+)*\s+.+", compact) and len(compact) <= 20:
        return True
    return len(compact) <= 8 and all(char.isdigit() or char in ".- " for char in compact)
