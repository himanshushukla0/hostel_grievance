import json

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

json_str = code.split('const DSA_DATA = ')[1].rsplit(';', 1)[0].rsplit(';\n', 1)[0]
data = json.loads(json_str)

# Global curated mappings for multi-source enrichment across topics
topic_enrichments = {
    # Step 1: Learn the basics
    "step-1": {
        "abdul_bari": "https://www.youtube.com/watch?v=9TlHvipP5yA", # Analysis of Algorithms & Asymptotic Notations
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
        "neetcode": "https://neetcode.io/practice",
        "visualgo": "https://visualgo.net/en"
    },
    # Step 2: Sorting Techniques
    "step-2": {
        "abdul_bari": "https://www.youtube.com/watch?v=pKK3A_V_eXg", # Merge Sort, Quick Sort, Selection Sort
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-3-sorting/",
        "neetcode": "https://neetcode.io/practice",
        "visualgo": "https://visualgo.net/en/sorting",
        "cp_algorithms": "https://cp-algorithms.com/sequences/rmq.html"
    },
    # Step 3: Arrays
    "step-3": {
        "neetcode": "https://neetcode.io/practice", # Arrays & Hashing, Two Pointers
        "abdul_bari": "https://www.youtube.com/watch?v=07ZfGz64f0Q",
        "usaco": "https://usaco.guide/silver/two-pointers",
        "visualgo": "https://visualgo.net/en/array",
        "cp_algorithms": "https://cp-algorithms.com/data_structures/fenwick.html"
    },
    # Step 4: Binary Search
    "step-4": {
        "neetcode": "https://neetcode.io/practice", # Binary Search
        "abdul_bari": "https://www.youtube.com/watch?v=C2apEw9pgtw",
        "usaco": "https://usaco.guide/silver/binary-search",
        "errichto": "https://www.youtube.com/watch?v=GU7DpgHINWQ",
        "cp_algorithms": "https://cp-algorithms.com/num_methods/binary_search.html"
    },
    # Step 5: Strings
    "step-5": {
        "neetcode": "https://neetcode.io/practice",
        "abdul_bari": "https://www.youtube.com/watch?v=V5-7GzOfADQ",
        "cp_algorithms": "https://cp-algorithms.com/string/string-hashing.html"
    },
    # Step 6: LinkedList
    "step-6": {
        "neetcode": "https://neetcode.io/practice",
        "abdul_bari": "https://www.youtube.com/watch?v=nobE_02I_w0",
        "william_fiset": "https://www.youtube.com/watch?v=njTh_OwMljA",
        "visualgo": "https://visualgo.net/en/list"
    },
    # Step 7: Recursion & Backtracking
    "step-7": {
        "abdul_bari": "https://www.youtube.com/watch?v=mBNrRy2_hVs", # Backtracking & Recursion Tree
        "neetcode": "https://neetcode.io/practice",
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-2-data-structures-and-dynamic-arrays/",
        "william_fiset": "https://www.youtube.com/watch?v=xFv_Hl4B83A",
        "visualgo": "https://visualgo.net/en/recursion"
    },
    # Step 8: Bit Manipulation
    "step-8": {
        "mit": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/resources/lecture-3-bit-hacks/",
        "neetcode": "https://neetcode.io/practice",
        "errichto": "https://www.youtube.com/watch?v=xXKL9YBWgCY",
        "cp_algorithms": "https://cp-algorithms.com/algebra/all-submasks.html",
        "usaco": "https://usaco.guide/silver/bitwise-ops"
    },
    # Step 9: Stacks and Queues
    "step-9": {
        "neetcode": "https://neetcode.io/practice",
        "abdul_bari": "https://www.youtube.com/watch?v=sFVxsglODoo",
        "william_fiset": "https://www.youtube.com/watch?v=RAMqDliI_a0",
        "usaco": "https://usaco.guide/gold/stacks",
        "cp_algorithms": "https://cp-algorithms.com/data_structures/stack_queue_modification.html",
        "visualgo": "https://visualgo.net/en/list"
    },
    # Step 10: Sliding Window & Two Pointer
    "step-10": {
        "neetcode": "https://neetcode.io/practice",
        "usaco": "https://usaco.guide/silver/two-pointers",
        "errichto": "https://www.youtube.com/watch?v=y_Y7Dq1xPZk",
        "cp_algorithms": "https://cp-algorithms.com/data_structures/stack_queue_modification.html"
    },
    # Step 11: Heaps
    "step-11": {
        "abdul_bari": "https://www.youtube.com/watch?v=HqPJF2L5h9U", # Heap Sort & Priority Queues
        "neetcode": "https://neetcode.io/practice",
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-8-heaps/",
        "william_fiset": "https://www.youtube.com/watch?v=wptevk0bshY",
        "visualgo": "https://visualgo.net/en/heap"
    },
    # Step 12: Greedy
    "step-12": {
        "abdul_bari": "https://www.youtube.com/watch?v=ARvQcqJ_-NY", # Fractional Knapsack, Job Sequencing
        "neetcode": "https://neetcode.io/practice",
        "mit": "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/lecture-16-greedy-algorithms-minimum-spanning-trees/",
        "usaco": "https://usaco.guide/silver/greedy-sorting"
    },
    # Step 13: Binary Trees
    "step-13": {
        "neetcode": "https://neetcode.io/practice",
        "abdul_bari": "https://www.youtube.com/watch?v=GzL-Zp7e1lU",
        "william_fiset": "https://www.youtube.com/watch?v=0qgaIMq8uHU",
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-5-binary-trees/",
        "visualgo": "https://visualgo.net/en/bst"
    },
    # Step 14: Binary Search Trees
    "step-14": {
        "neetcode": "https://neetcode.io/practice",
        "abdul_bari": "https://www.youtube.com/watch?v=5cPBt_P0a1Y",
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-6-binary-search-trees/",
        "william_fiset": "https://www.youtube.com/watch?v=1d3b_tPkWtA",
        "visualgo": "https://visualgo.net/en/bst"
    },
    # Step 15: Graphs
    "step-15": {
        "abdul_bari": "https://www.youtube.com/watch?v=pcKY4hjDrxk", # Dijkstra, Bellman-Ford, Prim, Kruskal
        "neetcode": "https://neetcode.io/practice",
        "william_fiset": "https://www.youtube.com/watch?v=09_LlHjoEiY",
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-9-breadth-first-search-bfs/",
        "usaco": "https://usaco.guide/gold/shortest-paths",
        "cp_algorithms": "https://cp-algorithms.com/graph/dijkstra.html",
        "visualgo": "https://visualgo.net/en/sssp"
    },
    # Step 16: Dynamic Programming
    "step-16": {
        "abdul_bari": "https://www.youtube.com/watch?v=5dRgrBgFx2w", # 0/1 Knapsack, LCS, Matrix Chain Multiplication
        "neetcode": "https://neetcode.io/practice",
        "mit": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-15-dynamic-programming/",
        "errichto": "https://www.youtube.com/watch?v=YBSt1jYwVfU",
        "usaco": "https://usaco.guide/gold/dp-intro",
        "cp_algorithms": "https://cp-algorithms.com/dynamic_programming/intro-to-dp.html"
    },
    # Step 17: Tries
    "step-17": {
        "neetcode": "https://neetcode.io/practice",
        "william_fiset": "https://www.youtube.com/watch?v=AXjmTQ8LEoI",
        "cp_algorithms": "https://cp-algorithms.com/data_structures/trie.html",
        "visualgo": "https://visualgo.net/en/suffixtree"
    },
    # Step 18: Strings Advanced
    "step-18": {
        "abdul_bari": "https://www.youtube.com/watch?v=V5-7GzOfADQ", # KMP Algorithm, Rabin Karp
        "cp_algorithms": "https://cp-algorithms.com/string/prefix-function.html",
        "errichto": "https://www.youtube.com/watch?v=1la_q_9eH8Y",
        "usaco": "https://usaco.guide/gold/string-hashing"
    },
    # Step 19: Quant & HFT Engineering
    "step-19": {
        "mit": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
        "cppreference": "https://en.cppreference.com/w/cpp/atomic/memory_order"
    },
    # Step 20: Quant Research
    "step-20": {
        "mit": "https://ocw.mit.edu/courses/18-440-probability-and-random-variables-spring-2014/"
    },
    # Step 21: Global Elite Problem Sets
    "step-21": {
        "cses": "https://cses.fi/problemset/",
        "usaco": "https://usaco.guide/"
    },
    # Step 22: Core CS & LLD
    "step-22": {
        "mit": "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/",
        "github": "https://github.com/ashishps1/awesome-low-level-design"
    }
}

# Iterate over all steps and enrich every problem
enriched_count = 0
for step in data:
    sid = step.get('stepId')
    enh = topic_enrichments.get(sid, {})
    
    for topic in step['topics']:
        for prob in topic['problems']:
            # Attach multi-source links if not already present
            for key, val in enh.items():
                if not prob.get(key):
                    prob[key] = val
            enriched_count += 1

print(f"Enriched {enriched_count} problems across all steps with multi-source global references!")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet + Multi-Source Global References (NeetCode, Abdul Bari, MIT, USACO, William Fiset, CP-Algorithms, Visualgo, Errichto)\n")
    f.write("const DSA_DATA = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")
