import requests
import re

with open('page_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all script src
scripts = re.findall(r'src="(/_next/static/chunks/[^"]+)"', html)
print(f"Found {len(scripts)} static script files")

base = "https://takeuforward.org"
headers = {'User-Agent': 'Mozilla/5.0'}

api_endpoints = set()
for s in scripts:
    url = base + s
    try:
        r = requests.get(url, headers=headers, timeout=5)
        text = r.text
        # Look for URLs or API paths
        matches = re.findall(r'["\'](https?://[^"\']+|/api/[^"\']+)["\']', text)
        for m in matches:
            if any(k in m for k in ['track', 'sheet', 'dsa', 'problem', 'subject', 'user', 'progress']):
                api_endpoints.add(m)
    except Exception as e:
        print(f"Error reading {s}: {e}")

print("Discovered API endpoints / paths:")
for ep in sorted(api_endpoints):
    print(" -", ep)
