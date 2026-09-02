import re

with open('full_tuf_raw_payload.txt', 'r', encoding='utf-8') as f:
    text = f.read()

keywords = ["Largest Element", "Kadane", "Two Sum", "Pascal", "Binary Search", "Merge Sort"]
for kw in keywords:
    pos = text.find(kw)
    if pos != -1:
        print(f"--- Context for '{kw}' (pos {pos}) ---")
        print(text[max(0, pos-200):min(len(text), pos+300)])
        print("\n" + "="*50 + "\n")
