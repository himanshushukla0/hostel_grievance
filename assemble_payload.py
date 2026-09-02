import re
import json

with open('course_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all self.__next_f.push scripts
chunks = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html, re.DOTALL)
print(f"Total Next.js streaming chunks found: {len(chunks)}")

raw_payload = ""
for c in chunks:
    try:
        # unescape json-string
        clean = json.loads(f'"{c}"')
        raw_payload += clean
    except Exception:
        clean = c.encode().decode('unicode_escape', errors='ignore')
        raw_payload += clean

with open('full_tuf_raw_payload.txt', 'w', encoding='utf-8') as pf:
    pf.write(raw_payload)

print(f"Full reconstructed payload length: {len(raw_payload)} characters")

# Find all occurrences of problem objects
# Let's inspect the JSON structures inside raw_payload
with open('parse_payload.py', 'w', encoding='utf-8') as f:
    f.write('''
import re, json

with open('full_tuf_raw_payload.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for patterns like {"title": ..., "difficulty": ...} or similar
print("Searching for problem patterns in raw payload...")

# Find all youtube / leetcode / takeuforward article links
yt_links = re.findall(r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+|https?://youtu\.be/[\w-]+', text)
lc_links = re.findall(r'https?://leetcode\.com/problems/[\w-]+/?', text)
tuf_articles = re.findall(r'https?://takeuforward\.org/[\w/-]+', text)

print(f"Unique YouTube videos: {len(set(yt_links))}")
print(f"Unique LeetCode links: {len(set(lc_links))}")
print(f"Unique TUF Articles: {len(set(tuf_articles))}")
''')
