
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
