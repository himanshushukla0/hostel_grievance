import re
import json

with open('scrape_course.py', 'r') as f:
    pass

import requests
r = requests.get('https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/', headers={'User-Agent': 'Mozilla/5.0'})

with open('course_page.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

print("Saved course_page.html, size:", len(r.text))

# Search for patterns or JSON scripts
scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
print(f"Found {len(scripts)} scripts")
for idx, s in enumerate(scripts):
    if len(s) > 500:
        print(f"Script {idx}: len {len(s)}")
        # check if it has problem data
        if any(w in s for w in ["Step", "Learn the basics", "Binary Search", "Dynamic Programming"]):
            print(f"--> Script {idx} contains DSA topics! Length: {len(s)}")
            with open(f'script_{idx}.js', 'w', encoding='utf-8') as sf:
                sf.write(s)
