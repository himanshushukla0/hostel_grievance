import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

url = 'https://takeuforward.org/dsa/strivers-a2z-dsa-track'
r = requests.get(url, headers=headers)
html = r.text

print('Fetched HTML length:', len(html))
with open('page_raw.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Extract RSC chunks
chunks = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html, re.DOTALL)
print(f'Total RSC chunks found: {len(chunks)}')

# Let's inspect chunks for topic names or problem titles
combined = ""
for c in chunks:
    clean = c.encode().decode('unicode_escape', errors='ignore')
    combined += clean + "\n"

with open('rsc_dump.txt', 'w', encoding='utf-8') as f:
    f.write(combined)

print('Dumped RSC data into rsc_dump.txt')
