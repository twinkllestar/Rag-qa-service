# input guard: detect injection / redact PII
# pure functions no side effects, easy to test
import re

# 常见的 injection 写法。re.IGNORECASE = 不区分大小写
INJECTION_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        # "ignore / disregard / forget ... previous / all / your ... instructions / rules"
        r"\b(ignore|disregard|forget|override)\b.{0,30}"
        r"\b(previous|prior|above|earlier|all|your)\b.{0,30}"
        r"\b(instructions?|prompts?|rules?|guidelines?)\b",
        # "reveal / show / print ... your system prompt"
        r"\b(reveal|show|print|repeat|output|leak)\b.{0,30}"
        r"\b(system prompt|system message|your instructions|your prompt)\b",
        r"\byou are now\b",
        r"\b(jailbreak|developer mode|dan mode)\b",
    ]
]

# PII 的 pattern。顺序很重要:先处理最具体的 (email、身份证),最后才是宽松的 (电话)
PII_PATTERNS = [
    ("[EMAIL]", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("[ID_NUMBER]", re.compile(r"\b\d{17}[\dXx]\b")),  # 18 位身份证号
    ("[PHONE]", re.compile(r"\+?\d[\d\s().-]{7,}\d")),
]


def looks_like_injection(text: str) -> bool:
    # first check for common injection patterns，invoid "ignore    previous"
    normalized = " ".join(text.split())
    return any(p.search(normalized) for p in INJECTION_PATTERNS)


def redact_pii(text: str) -> tuple[str, int]:
    # return (redacted_text, total_count_of_replacements)
    total = 0
    for placeholder, pattern in PII_PATTERNS:
        text, count = pattern.subn(placeholder, text)
        total += count
    return text, total