import json

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

json_str = code.split('const DSA_DATA = ')[1].rsplit(';', 1)[0].rsplit(';\n', 1)[0]
data = json.loads(json_str)

max_id = 0
for s in data:
    for t in s['topics']:
        for p in t['problems']:
            if p.get('id', 0) > max_id:
                max_id = p.get('id', 0)

print(f"Current max ID: {max_id}, Current Steps: {len(data)}")

step_21 = {
  "stepId": "step-21",
  "stepTitle": "Step 21: Global Elite Problem Sets & Olympiad Benchmarks [CSES, USACO & MIT]",
  "description": "The gold-standard benchmark problems practiced by ICPC World Finalists, USA Olympiad competitors, and Top HFT engineers.",
  "topics": [
    {
      "subtopic": "CSES 300 Global Algorithmic Benchmarks (Helsinki)",
      "problems": [
        {
          "id": max_id + 1,
          "title": "CSES: Weird Algorithm & Collatz Conjecture (Introductory Benchmark)",
          "difficulty": "Easy",
          "link": "https://cses.fi/problemset/task/1068",
          "article": "https://usaco.guide/general/intro-cses",
          "youtube": "https://www.youtube.com/watch?v=0_3rO50B59E",
          "leetcode": None
        },
        {
          "id": max_id + 2,
          "title": "CSES: Ferris Wheel & Greedy Two-Pointer Optimization",
          "difficulty": "Easy",
          "link": "https://cses.fi/problemset/task/1090",
          "article": "https://usaco.guide/silver/two-pointers",
          "youtube": "https://www.youtube.com/watch?v=5rT8gW1vD5E",
          "leetcode": None
        },
        {
          "id": max_id + 3,
          "title": "CSES: Dice Combinations & Coin Combinations I & II (DP State Transition Benchmark)",
          "difficulty": "Medium",
          "link": "https://cses.fi/problemset/task/1633",
          "article": "https://usaco.guide/gold/paths-grids",
          "youtube": "https://www.youtube.com/watch?v=KzZ_O8jA8l4",
          "leetcode": "https://leetcode.com/problems/coin-change/"
        },
        {
          "id": max_id + 4,
          "title": "CSES: Static Range Minimum Queries & Segment Tree / Fenwick Tree Construction",
          "difficulty": "Hard",
          "link": "https://cses.fi/problemset/task/1647",
          "article": "https://cp-algorithms.com/data_structures/segment_tree.html",
          "youtube": "https://www.youtube.com/watch?v=ZBHKZF5w440",
          "leetcode": "https://leetcode.com/problems/range-sum-query-mutable/"
        },
        {
          "id": max_id + 5,
          "title": "CSES: Labyrinth & Shortest Path in 2D Grid with BFS / Path Reconstruction",
          "difficulty": "Medium",
          "link": "https://cses.fi/problemset/task/1193",
          "article": "https://usaco.guide/silver/graph-traversal",
          "youtube": "https://www.youtube.com/watch?v=34dJv6gQ_nE",
          "leetcode": "https://leetcode.com/problems/shortest-path-in-binary-matrix/"
        }
      ]
    },
    {
      "subtopic": "USACO Olympiad Advanced C++ Curriculum",
      "problems": [
        {
          "id": max_id + 6,
          "title": "USACO Silver: Coordinate Compression & Multi-Dimensional Prefix Sums",
          "difficulty": "Medium",
          "link": "https://usaco.guide/silver/prefix-sums",
          "article": "https://usaco.guide/silver/prefix-sums",
          "youtube": "https://www.youtube.com/watch?v=p1hD1a5x0XU",
          "leetcode": None
        },
        {
          "id": max_id + 7,
          "title": "USACO Gold: Binary Lifting for Tree Lowest Common Ancestor (LCA in O(log N))",
          "difficulty": "Hard",
          "link": "https://usaco.guide/gold/tree-euler",
          "article": "https://cp-algorithms.com/graph/lca_binary_lifting.html",
          "youtube": "https://www.youtube.com/watch?v=kOfb_42wFVM",
          "leetcode": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/"
        },
        {
          "id": max_id + 8,
          "title": "USACO Gold: Disjoint Set Union (DSU) with Union-by-Rank & Path Compression",
          "difficulty": "Medium",
          "link": "https://usaco.guide/gold/dsu",
          "article": "https://cp-algorithms.com/data_structures/disjoint_set_union.html",
          "youtube": "https://www.youtube.com/watch?v=ayW5B2W9hfo",
          "leetcode": "https://leetcode.com/problems/redundant-connection/"
        }
      ]
    },
    {
      "subtopic": "Abdul Bari & MIT 6.006 Theory Proofs",
      "problems": [
        {
          "id": max_id + 9,
          "title": "Abdul Bari Masterclass: Recurrence Relations & The Master Theorem Proofs",
          "difficulty": "Easy",
          "link": "https://www.youtube.com/watch?v=2Rr2tW9zvRg",
          "article": "https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)",
          "youtube": "https://www.youtube.com/watch?v=2Rr2tW9zvRg",
          "leetcode": None
        },
        {
          "id": max_id + 10,
          "title": "MIT 6.006: Balanced Search Trees, AVL Tree Rotations & Invariant Proofs",
          "difficulty": "Hard",
          "link": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
          "article": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
          "youtube": "https://www.youtube.com/watch?v=vURtCXQn2MQ",
          "leetcode": None
        }
      ]
    }
  ]
}

has_step_21 = any(s['stepId'] == 'step-21' for s in data)
if not has_step_21:
    data.append(step_21)
    print("Appended Step 21: Global Elite Problem Sets & Olympiad Benchmarks!")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet + Integrated Quant/HFT + Global Elite Benchmarks\n")
    f.write("const DSA_DATA = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

total = sum(len(t['problems']) for s in data for t in s['topics'])
print(f"Grand Total Problems in Vault: {total}")
