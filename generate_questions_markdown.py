import json

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

json_str = code.split('const DSA_DATA = ')[1].rsplit(';', 1)[0].rsplit(';\n', 1)[0]
data = json.loads(json_str)

md_lines = []
md_lines.append("# 🚀 A2Z DSA, NeetCode 150, Blind 75 & Quant Placement Master Curriculum")
md_lines.append("\n> **Total Steps:** 22 | **Total Problems / Interview Units:** 590\n")
md_lines.append("Complete structured master list of every single problem, interview concept, and multi-source video breakdown across Striver A2Z, NeetCode 150, Blind 75, Abdul Bari Algorithm Proofs, MIT OCW, USACO Olympiad, and Core CS Subjects.\n")
md_lines.append("---")

total_count = 0

for step_idx, step in enumerate(data, 1):
    step_title = step.get('stepTitle', f"Step {step_idx}")
    step_desc = step.get('description', '')
    step_probs_count = sum(len(t.get('problems', [])) for t in step.get('topics', []))
    
    md_lines.append(f"\n## 📌 {step_title} ({step_probs_count} Problems)")
    if step_desc:
        md_lines.append(f"*{step_desc}*\n")
    
    for topic in step.get('topics', []):
        subtopic = topic.get('subtopic', 'General')
        problems = topic.get('problems', [])
        md_lines.append(f"\n### 🔹 {subtopic}")
        md_lines.append("| ID | Problem / Topic | Diff | Badges | Practice Link | Solution / Video Lecture |")
        md_lines.append("| :--- | :--- | :---: | :---: | :--- | :--- |")
        
        for p in problems:
            total_count += 1
            pid = p.get('id', total_count)
            title = p.get('title', 'Untitled')
            diff = p.get('difficulty', 'Medium')
            
            badges = []
            if p.get('isBlind75'):
                badges.append("🔥 Blind 75")
            elif p.get('isNeetCode'):
                badges.append("⚡ NeetCode 150")
            badge_str = " ".join(badges) if badges else "-"
            
            link = p.get('link') or p.get('leetcode') or '#'
            clean_link = f"[{title}]({link})"
            
            resources = []
            if p.get('youtube'):
                resources.append(f"[TUF Video]({p['youtube']})")
            if p.get('neetcode'):
                resources.append(f"[NeetCode]({p['neetcode']})")
            if p.get('abdul_bari'):
                resources.append(f"[Abdul Bari]({p['abdul_bari']})")
            if p.get('mit'):
                resources.append(f"[MIT OCW]({p['mit']})")
            if p.get('william_fiset'):
                resources.append(f"[William Fiset]({p['william_fiset']})")
            if p.get('cp_algorithms'):
                resources.append(f"[CP-Algorithms]({p['cp_algorithms']})")
            if p.get('visualgo'):
                resources.append(f"[Visualgo]({p['visualgo']})")
            if p.get('errichto'):
                resources.append(f"[Errichto]({p['errichto']})")
            if p.get('usaco'):
                resources.append(f"[USACO]({p['usaco']})")
            if p.get('article'):
                resources.append(f"[Article]({p['article']})")
            
            res_str = " • ".join(resources) if resources else "-"
            
            # Format diff emoji
            diff_icon = "🟢 Easy" if diff == "Easy" else ("🟡 Medium" if diff == "Medium" else "🔴 Hard")
            
            # Escape pipes in title
            clean_title = title.replace('|', '/')
            md_lines.append(f"| `{pid}` | **{clean_title}** | {diff_icon} | {badge_str} | [Solve Here]({link}) | {res_str} |")

with open('QUESTIONS_MASTER_LIST.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print(f"Generated QUESTIONS_MASTER_LIST.md with {total_count} questions across {len(data)} steps!")

# Also generate clean JSON export
with open('DSA_COMPLETE_QUESTIONS.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Generated DSA_COMPLETE_QUESTIONS.json!")
