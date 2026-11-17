# 检查 answerable 的 expected_any 关键词是否真的出现在 data/docs 里。
# 运行方式 (项目根目录): python -m scripts.check_cases
import json
from pathlib import Path

corpus = " ".join(
    p.read_text(encoding="utf-8") for p in Path("data/docs").glob("*.md")
).lower()

cases = json.loads(Path("data/eval/cases.json").read_text(encoding="utf-8"))
problems = 0
for case in cases:
    if case["category"] != "answerable":
        continue
    found = [k for k in case["expected_any"] if k.lower() in corpus]
    if not found:
        problems += 1
        print(f"NOT IN DOCS: {case['question']}  keywords={case['expected_any']}")

print(f"\nChecked. {problems} case(s) need attention.")