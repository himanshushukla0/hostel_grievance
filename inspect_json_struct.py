import re
import json

with open('full_tuf_raw_payload.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect a few sample problem blocks in the payload
print("Payload sample (around a problem):")
sample_match = re.search(r'\{[^{}]*?"title":\s*"[^"]+?"[^{}]*?\}', text)
if sample_match:
    print("Direct object found:", sample_match.group(0))

# Or find where steps are defined
step_matches = re.findall(r'(Step\s*\d+[^"\'<>\n\r]+)', text)
print("Steps found in text:", set(step_matches[:10]))
