import re
import json

with open('rsc_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("Dump length:", len(text))
# Search for keywords like "problems", "title", "subject", "topics", "step"
keywords = ["solved_problem_ids", "steps", "topics", "sub_topics", "difficulty", "youtube", "article", "leetcode"]
for kw in keywords:
    pos = [m.start() for m in re.finditer(kw, text, re.IGNORECASE)]
    print(f"Keyword '{kw}': {len(pos)} occurrences")

# Find JSON-like object snippets
lines = text.split("\n")
for l in lines[:20]:
    if len(l.strip()) > 0:
        print("Line:", l[:120])
