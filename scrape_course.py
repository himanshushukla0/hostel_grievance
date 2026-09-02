import sys
import os
import re
import json
import requests

# Ensure UTF-8 output encoding for Windows PowerShell/CMD
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def scrape_takeuforward():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    sheet_url = 'https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/'
    print(f"[+] Fetching live TakeUForward course page from: {sheet_url}")
    
    html_text = ""
    try:
        r = requests.get(sheet_url, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.text) > 10000:
            html_text = r.text
            print(f"[OK] Successfully fetched live page (status {r.status_code}, {len(html_text):,} bytes)")
        else:
            print(f"[WARN] Live fetch returned status {r.status_code}. Using local cache fallback...")
    except Exception as e:
        print(f"[WARN] Live request error: {e}. Checking local cache fallback...")

    if not html_text and os.path.exists('course_page.html'):
        with open('course_page.html', 'r', encoding='utf-8', errors='ignore') as f:
            html_text = f.read()
        print(f"[FILE] Loaded cached 'course_page.html' ({len(html_text):,} bytes)")

    if not html_text:
        print("[ERR] Error: Could not obtain TakeUForward course page HTML.")
        return

    # TakeUForward is built on Next.js App Router (RSC - React Server Components).
    # The problem hierarchy is streamed across self.__next_f.push([1, "..."]) script tags.
    print("\n[INFO] Extracting and assembling React Server Component (RSC) chunks...")
    
    chunk_pattern = re.compile(r'self\.__next_f\.push\(\[\s*\d+\s*,\s*(".*?")\s*\]\)', re.DOTALL)
    raw_chunks = chunk_pattern.findall(html_text)
    print(f"[OK] Found {len(raw_chunks)} RSC payload chunks.")

    # Decode and concatenate string chunks
    full_payload = []
    for chunk in raw_chunks:
        try:
            decoded = json.loads(chunk)
            full_payload.append(decoded)
        except Exception:
            full_payload.append(chunk[1:-1])

    assembled_text = "".join(full_payload)
    print(f"[OK] Assembled complete stream payload ({len(assembled_text):,} characters).")

    # Locate sections / categories in the assembled payload
    start_key = None
    for key in ['"sections":[', '"categories":[', 'sections:[', 'categories:[']:
        idx = assembled_text.find(key)
        if idx != -1:
            start_key = key
            start_idx = idx
            break

    if not start_key:
        print("[ERR] Could not locate 'sections' or 'categories' array in payload stream.")
        return

    print(f"[OK] Found data starting with key '{start_key}' at index {start_idx}.")
    slice_text = assembled_text[start_idx + len(start_key) - 1:] # start from '['

    # Robust JSON Bracket depth matcher
    bracket_depth = 0
    array_end = -1
    in_string = False
    escape = False

    for i, ch in enumerate(slice_text):
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch == '[':
                bracket_depth += 1
            elif ch == ']':
                bracket_depth -= 1
                if bracket_depth == 0:
                    array_end = i + 1
                    break

    if array_end == -1:
        print("[ERR] Could not match closing bracket for array.")
        return

    raw_categories_json = slice_text[:array_end]
    # Sanitize Next.js "$undefined" tokens
    clean_json = raw_categories_json.replace('"$undefined"', 'null').replace('$undefined', 'null')

    try:
        categories = json.loads(clean_json)
        print(f"\n[SUCCESS] Successfully parsed {len(categories)} Steps from TakeUForward Sheet!\n" + "="*70)

        total_topics = 0
        total_problems = 0
        transformed_catalog = []

        for step_idx, step in enumerate(categories, start=1):
            step_name = step.get('category_name', step.get('title', f'Step {step_idx}'))
            subcategories = step.get('subcategories', step.get('topics', []))
            
            step_obj = {
                "stepId": f"step-{step_idx}",
                "stepTitle": f"Step {step_idx}: {step_name}",
                "topics": []
            }

            step_prob_count = 0
            for topic in subcategories:
                topic_name = topic.get('subcategory_name', topic.get('topic_name', 'Topic'))
                problems = topic.get('problems', [])
                step_prob_count += len(problems)
                
                topic_obj = {
                    "subtopic": topic_name,
                    "problems": []
                }

                for prob in problems:
                    p_id = prob.get('problem_id', prob.get('id'))
                    p_title = prob.get('problem_name', prob.get('title', ''))
                    p_diff = prob.get('difficulty', 'Medium')
                    p_link = prob.get('link') or prob.get('article') or prob.get('plus')
                    if p_link and str(p_link).startswith('/'):
                        p_link = f"https://takeuforward.org{p_link}"

                    topic_obj["problems"].append({
                        "id": p_id,
                        "title": p_title,
                        "difficulty": p_diff,
                        "link": p_link,
                        "article": prob.get('article'),
                        "youtube": prob.get('youtube'),
                        "leetcode": prob.get('leetcode'),
                        "plus": prob.get('plus')
                    })

                step_obj["topics"].append(topic_obj)

            total_topics += len(subcategories)
            total_problems += step_prob_count
            transformed_catalog.append(step_obj)
            print(f" [Step {step_idx:2d}] {step_name:<38} | {len(subcategories):2d} subtopics | {step_prob_count:3d} problems")

        print("="*70)
        print(f"[SUMMARY] Extraction Results:")
        print(f"   • Total Steps:      {len(categories)}")
        print(f"   • Total Subtopics:  {total_topics}")
        print(f"   • Total Problems:   {total_problems}")

        # Save output JSON
        output_file = 'tuf_scraped_output.json'
        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(transformed_catalog, out_f, indent=2, ensure_ascii=False)
        print(f"\n[SAVED] Saved structured catalog to '{output_file}'!")

    except Exception as err:
        print("[ERR] JSON decoding error:", err)

if __name__ == '__main__':
    scrape_takeuforward()
