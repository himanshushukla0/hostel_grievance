import re
import json

with open('full_tuf_raw_payload.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the start of the entire categories list:
# It starts around the first 'category_id":"683"'
first_cat = text.find('{"category_id":"683"')
if first_cat == -1:
    first_cat = text.find('{"category_id"')
    
print("First category index:", first_cat)

# We can parse the array or find all JSON objects with category_id
# Let's find each category object using balanced braces
categories = []
pattern = r'\{"category_id":\s*"\d+",\s*"category_name":\s*"[^"]+?",\s*"subcategories":\s*\['

match_starts = [m.start() for m in re.finditer(pattern, text)]
print(f"Found {len(match_starts)} category start positions")

for idx, start_pos in enumerate(match_starts):
    # Find end of category object with bracket counting
    bracket_depth = 0
    in_string = False
    escape = False
    end_pos = -1
    
    for i in range(start_pos, len(text)):
        ch = text[i]
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
            if ch == '{':
                bracket_depth += 1
            elif ch == '}':
                bracket_depth -= 1
                if bracket_depth == 0:
                    end_pos = i + 1
                    break
                    
    if end_pos != -1:
        cat_json_str = text[start_pos:end_pos]
        # replace $undefined
        clean_json_str = cat_json_str.replace('"$undefined"', 'null').replace('$undefined', 'null')
        try:
            cat_obj = json.loads(clean_json_str)
            categories.append(cat_obj)
        except Exception as e:
            print(f"Failed parsing category {idx+1}: {e}")

print(f"Successfully extracted {len(categories)} categories!")

# Let's count total problems and inspect details
total_problems = 0
transformed_steps = []

for step_idx, cat in enumerate(categories, 1):
    step_name = cat.get('category_name', f'Step {step_idx}')
    step_id = f"step-{step_idx}"
    subcategories = cat.get('subcategories', [])
    step_problems_count = 0
    topics_list = []
    
    for sub in subcategories:
        sub_name = sub.get('subcategory_name', 'General')
        sub_problems = []
        
        for p in sub.get('problems', []):
            total_problems += 1
            step_problems_count += 1
            
            p_id = int(p.get('problem_id', total_problems))
            p_name = p.get('problem_name', '').strip()
            difficulty = p.get('difficulty', 'Easy')
            if difficulty not in ['Easy', 'Medium', 'Hard']:
                difficulty = 'Easy'
                
            article = p.get('article')
            youtube = p.get('youtube')
            leetcode = p.get('leetcode')
            plus = p.get('plus')
            
            primary_link = leetcode if leetcode and leetcode != 'null' else (article if article and article != 'null' else f"https://takeuforward.org/plus{plus}" if plus else "https://takeuforward.org")
            
            sub_problems.append({
                "id": p_id,
                "title": p_name,
                "difficulty": difficulty,
                "link": primary_link,
                "leetcode": leetcode if leetcode != 'null' else None,
                "article": article if article != 'null' else None,
                "youtube": youtube if youtube != 'null' else None,
                "plus": f"https://takeuforward.org{plus}" if plus and plus != 'null' else None
            })
            
        topics_list.append({
            "subtopic": sub_name,
            "problems": sub_problems
        })
        
    print(f"{step_name}: {step_problems_count} problems")
    
    transformed_steps.append({
        "stepId": step_id,
        "stepTitle": f"Step {step_idx}: {step_name}" if not step_name.lower().startswith('step') else step_name,
        "description": f"Master {step_name} with complete video tutorials, notes, and curated practice.",
        "topics": topics_list
    })

print(f"\nGRAND TOTAL PROBLEMS EXTRACTED: {total_problems}")

# Write to tuf_complete_sheet.json
with open('tuf_complete_sheet.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, indent=2, ensure_ascii=False)

# Write to data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet - 100% Authentic Full Dataset Extracted Directly from TakeUForward\n")
    f.write("const DSA_DATA = ")
    json.dump(transformed_steps, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

print("\nSaved 100% authentic data to tuf_complete_sheet.json and data.js!")
