import re

with open('full_tuf_raw_payload.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for matches of category_id or categories
matches = [m.start() for m in re.finditer(r'categories', text, re.IGNORECASE)]
print(f"Matches for 'categories': {len(matches)}")
for m in matches[:5]:
    print("Match around:", text[max(0, m-50):min(len(text), m+100)])
    print("-" * 40)
