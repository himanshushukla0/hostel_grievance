import re
import json

with open('full_tuf_raw_payload.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the categories array
# In the payload: it starts with something like {"categories":[...]} or "categories":[...]
start_idx = text.find('"categories":[')
if start_idx == -1:
    start_idx = text.find('categories:[')
    
print("Found 'categories' at index:", start_idx)

# Let's write a robust parser to extract the JSON array of categories
# We can find the matching closing bracket or parse with json
slice_text = text[start_idx:]
# Remove prefix
if slice_text.startswith('"categories":'):
    slice_text = slice_text[len('"categories":'):]

# Find where the array closes
# Count brackets
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

if array_end != -1:
    raw_categories_json = slice_text[:array_end]
    print(f"Extracted categories JSON slice of length: {len(raw_categories_json)}")
    
    # Replace "$undefined" with null so JSON is valid
    valid_json_str = raw_categories_json.replace('"$undefined"', 'null').replace('$undefined', 'null')
    
    try:
        categories_data = json.loads(valid_json_str)
        print(f"Successfully parsed {len(categories_data)} categories from TakeUForward!")
        
        total_probs = 0
        transformed_steps = []
        
        for cat_idx, cat in enumerate(categories_data, 1):
            step_id = f"step-{cat_idx}"
            step_title = cat.get('category_name', f"Step {cat_idx}")
            topics_list = []
            
            for sub in cat.get('subcategories', []):
                subtopic_name = sub.get('subcategory_name', 'General')
                sub_problems = []
                
                for p in sub.get('problems', []):
                    total_probs += 1
                    prob_id = int(p.get('problem_id', total_probs))
                    prob_title = p.get('problem_name', '').strip()
                    difficulty = p.get('difficulty', 'Easy')
                    if difficulty not in ['Easy', 'Medium', 'Hard']:
                        difficulty = 'Easy'
                        
                    article = p.get('article')
                    youtube = p.get('youtube')
                    leetcode = p.get('leetcode')
                    plus = p.get('plus')
                    
                    # Choose primary link
                    primary_link = leetcode or article or (f"https://takeuforward.org{plus}" if plus else "https://takeuforward.org")
                    
                    sub_problems.append({
                        "id": prob_id,
                        "title": prob_title,
                        "difficulty": difficulty,
                        "link": primary_link,
                        "leetcode": leetcode,
                        "article": article,
                        "youtube": youtube,
                        "plus": f"https://takeuforward.org{plus}" if plus else None
                    })
                
                topics_list.append({
                    "subtopic": subtopic_name,
                    "problems": sub_problems
                })
            
            transformed_steps.append({
                "stepId": step_id,
                "stepTitle": step_title,
                "description": f"Comprehensive problem set for {step_title}",
                "topics": topics_list
            })
            
        print(f"Total problems parsed from official TUF payload: {total_probs}")
        
        # Save complete raw JSON
        with open('tuf_complete_sheet.json', 'w', encoding='utf-8') as jf:
            json.dump(categories_data, jf, indent=2, ensure_ascii=False)
            
        # Update data.js
        with open('data.js', 'w', encoding='utf-8') as df:
            df.write("// Striver's A2Z DSA Sheet - 100% Official Raw Payload Extracted from TakeUForward\n")
            df.write("const DSA_DATA = ")
            json.dump(transformed_steps, df, indent=2, ensure_ascii=False)
            df.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")
            
        print("Successfully written tuf_complete_sheet.json and data.js!")
        
    except Exception as e:
        print("JSON parse error:", e)
        with open('debug_slice.json', 'w', encoding='utf-8') as dbg:
            dbg.write(valid_json_str[:5000])
else:
    print("Could not find array end.")
