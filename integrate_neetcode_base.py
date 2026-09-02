import json

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

json_str = code.split('const DSA_DATA = ')[1].rsplit(';', 1)[0].rsplit(';\n', 1)[0]
data = json.loads(json_str)

# Find max ID
max_id = 0
for s in data:
    for t in s['topics']:
        for p in t['problems']:
            if p.get('id', 0) > max_id:
                max_id = p.get('id', 0)

print(f"Current max ID: {max_id}, Total Steps: {len(data)}")

# Core NeetCode 150 & Blind 75 Problem Dataset with Direct YouTube Videos & LeetCode URLs
neetcode_150_dataset = [
    # Arrays & Hashing
    {"title": "Contains Duplicate", "diff": "Easy", "step": "step-3", "subtopic": "⚡ NeetCode 150: Arrays & Hashing Patterns", "lc": "https://leetcode.com/problems/contains-duplicate/", "yt": "https://www.youtube.com/watch?v=3OamzN90kPg", "blind75": True},
    {"title": "Valid Anagram", "diff": "Easy", "step": "step-5", "subtopic": "⚡ NeetCode 150: String Patterns", "lc": "https://leetcode.com/problems/valid-anagram/", "yt": "https://www.youtube.com/watch?v=9UtIn4vx9it", "blind75": True},
    {"title": "Two Sum", "diff": "Easy", "step": "step-3", "subtopic": "⚡ NeetCode 150: Arrays & Hashing Patterns", "lc": "https://leetcode.com/problems/two-sum/", "yt": "https://www.youtube.com/watch?v=KLlXCFG5TnA", "blind75": True},
    {"title": "Group Anagrams", "diff": "Medium", "step": "step-5", "subtopic": "⚡ NeetCode 150: String Patterns", "lc": "https://leetcode.com/problems/group-anagrams/", "yt": "https://www.youtube.com/watch?v=vzdNOK2oDAw", "blind75": True},
    {"title": "Top K Frequent Elements", "diff": "Medium", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/top-k-frequent-elements/", "yt": "https://www.youtube.com/watch?v=YPTqKIgVk-k", "blind75": True},
    {"title": "Product of Array Except Self", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Arrays & Hashing Patterns", "lc": "https://leetcode.com/problems/product-of-array-except-self/", "yt": "https://www.youtube.com/watch?v=bNvIQI2wAjk", "blind75": True},
    {"title": "Valid Sudoku", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Arrays & Hashing Patterns", "lc": "https://leetcode.com/problems/valid-sudoku/", "yt": "https://www.youtube.com/watch?v=TjFXEUCMqI8", "blind75": False},
    {"title": "Encode and Decode Strings", "diff": "Medium", "step": "step-5", "subtopic": "⚡ NeetCode 150: String Patterns", "lc": "https://leetcode.com/problems/encode-and-decode-strings/", "yt": "https://www.youtube.com/watch?v=B1k_sxOSgv8", "blind75": True},
    {"title": "Longest Consecutive Sequence", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Arrays & Hashing Patterns", "lc": "https://leetcode.com/problems/longest-consecutive-sequence/", "yt": "https://www.youtube.com/watch?v=P6RZZMu_maU", "blind75": True},

    # Two Pointers
    {"title": "Valid Palindrome", "diff": "Easy", "step": "step-5", "subtopic": "⚡ NeetCode 150: Two Pointer Patterns", "lc": "https://leetcode.com/problems/valid-palindrome/", "yt": "https://www.youtube.com/watch?v=jJXJ16kPFWg", "blind75": True},
    {"title": "Two Sum II - Input Array Is Sorted", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Two Pointer Patterns", "lc": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/", "yt": "https://www.youtube.com/watch?v=cQ1Oz4ckcMT", "blind75": False},
    {"title": "3Sum", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Two Pointer Patterns", "lc": "https://leetcode.com/problems/3sum/", "yt": "https://www.youtube.com/watch?v=jzZsG8n2R9A", "blind75": True},
    {"title": "Container With Most Water", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Two Pointer Patterns", "lc": "https://leetcode.com/problems/container-with-most-water/", "yt": "https://www.youtube.com/watch?v=UuiTKBwPgAo", "blind75": True},
    {"title": "Trapping Rain Water", "diff": "Hard", "step": "step-9", "subtopic": "⚡ NeetCode 150: Two Pointer & Stack Patterns", "lc": "https://leetcode.com/problems/trapping-rain-water/", "yt": "https://www.youtube.com/watch?v=ZI2z5pq0TqA", "blind75": True},

    # Sliding Window
    {"title": "Best Time to Buy and Sell Stock", "diff": "Easy", "step": "step-3", "subtopic": "⚡ NeetCode 150: Sliding Window Patterns", "lc": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "yt": "https://www.youtube.com/watch?v=1pkOGcDnxAM", "blind75": True},
    {"title": "Longest Substring Without Repeating Characters", "diff": "Medium", "step": "step-10", "subtopic": "⚡ NeetCode 150: Sliding Window Patterns", "lc": "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "yt": "https://www.youtube.com/watch?v=wiGpQwVHdE0", "blind75": True},
    {"title": "Longest Repeating Character Replacement", "diff": "Medium", "step": "step-10", "subtopic": "⚡ NeetCode 150: Sliding Window Patterns", "lc": "https://leetcode.com/problems/longest-repeating-character-replacement/", "yt": "https://www.youtube.com/watch?v=gqXU1UyA8pk", "blind75": True},
    {"title": "Permutation in String", "diff": "Medium", "step": "step-10", "subtopic": "⚡ NeetCode 150: Sliding Window Patterns", "lc": "https://leetcode.com/problems/permutation-in-string/", "yt": "https://www.youtube.com/watch?v=UbyhOgBNlyo", "blind75": False},
    {"title": "Minimum Window Substring", "diff": "Hard", "step": "step-10", "subtopic": "⚡ NeetCode 150: Sliding Window Patterns", "lc": "https://leetcode.com/problems/minimum-window-substring/", "yt": "https://www.youtube.com/watch?v=jSto0O4AJbM", "blind75": True},
    {"title": "Sliding Window Maximum", "diff": "Hard", "step": "step-10", "subtopic": "⚡ NeetCode 150: Sliding Window Patterns", "lc": "https://leetcode.com/problems/sliding-window-maximum/", "yt": "https://www.youtube.com/watch?v=DfljaUwZsOk", "blind75": False},

    # Stack
    {"title": "Valid Parentheses", "diff": "Easy", "step": "step-9", "subtopic": "⚡ NeetCode 150: Stack Patterns", "lc": "https://leetcode.com/problems/valid-parentheses/", "yt": "https://www.youtube.com/watch?v=WTzjTskDFMg", "blind75": True},
    {"title": "Min Stack", "diff": "Medium", "step": "step-9", "subtopic": "⚡ NeetCode 150: Stack Patterns", "lc": "https://leetcode.com/problems/min-stack/", "yt": "https://www.youtube.com/watch?v=qkLl7nAwDPo", "blind75": True},
    {"title": "Evaluate Reverse Polish Notation", "diff": "Medium", "step": "step-9", "subtopic": "⚡ NeetCode 150: Stack Patterns", "lc": "https://leetcode.com/problems/evaluate-reverse-polish-notation/", "yt": "https://www.youtube.com/watch?v=iu00Oj9G1Y0", "blind75": False},
    {"title": "Generate Parentheses", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/generate-parentheses/", "yt": "https://www.youtube.com/watch?v=s9fokUqJ76A", "blind75": False},
    {"title": "Daily Temperatures", "diff": "Medium", "step": "step-9", "subtopic": "⚡ NeetCode 150: Stack Patterns", "lc": "https://leetcode.com/problems/daily-temperatures/", "yt": "https://www.youtube.com/watch?v=cTBiBSnjO3c", "blind75": False},
    {"title": "Car Fleet", "diff": "Medium", "step": "step-9", "subtopic": "⚡ NeetCode 150: Stack Patterns", "lc": "https://leetcode.com/problems/car-fleet/", "yt": "https://www.youtube.com/watch?v=Pr6T-3yB9RM", "blind75": False},
    {"title": "Largest Rectangle in Histogram", "diff": "Hard", "step": "step-9", "subtopic": "⚡ NeetCode 150: Stack Patterns", "lc": "https://leetcode.com/problems/largest-rectangle-in-histogram/", "yt": "https://www.youtube.com/watch?v=zx5SwR13040", "blind75": False},

    # Binary Search
    {"title": "Binary Search", "diff": "Easy", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/binary-search/", "yt": "https://www.youtube.com/watch?v=s4D94WiTErq", "blind75": False},
    {"title": "Search a 2D Matrix", "diff": "Medium", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/search-a-2d-matrix/", "yt": "https://www.youtube.com/watch?v=Ber2pi2C0j0", "blind75": True},
    {"title": "Koko Eating Bananas", "diff": "Medium", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/koko-eating-bananas/", "yt": "https://www.youtube.com/watch?v=U2SozAs9RzA", "blind75": False},
    {"title": "Find Minimum in Rotated Sorted Array", "diff": "Medium", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/", "yt": "https://www.youtube.com/watch?v=nIVW4P8b1VA", "blind75": True},
    {"title": "Search in Rotated Sorted Array", "diff": "Medium", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/search-in-rotated-sorted-array/", "yt": "https://www.youtube.com/watch?v=U8XENwh8Oy8", "blind75": True},
    {"title": "Time Based Key-Value Store", "diff": "Medium", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/time-based-key-value-store/", "yt": "https://www.youtube.com/watch?v=fu2cD_6E8Hw", "blind75": False},
    {"title": "Median of Two Sorted Arrays", "diff": "Hard", "step": "step-4", "subtopic": "⚡ NeetCode 150: Binary Search Patterns", "lc": "https://leetcode.com/problems/median-of-two-sorted-arrays/", "yt": "https://www.youtube.com/watch?v=q6IEA26hvPE", "blind75": False},

    # Linked List
    {"title": "Reverse Linked List", "diff": "Easy", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/reverse-linked-list/", "yt": "https://www.youtube.com/watch?v=G0_I-ZF0S38", "blind75": True},
    {"title": "Merge Two Sorted Lists", "diff": "Easy", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/merge-two-sorted-lists/", "yt": "https://www.youtube.com/watch?v=XIdigk956u0", "blind75": True},
    {"title": "Reorder List", "diff": "Medium", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/reorder-list/", "yt": "https://www.youtube.com/watch?v=S5bfdUTrKLc", "blind75": True},
    {"title": "Remove Nth Node From End of List", "diff": "Medium", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/", "yt": "https://www.youtube.com/watch?v=XVuQxVej6y8", "blind75": True},
    {"title": "Copy List with Random Pointer", "diff": "Medium", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/copy-list-with-random-pointer/", "yt": "https://www.youtube.com/watch?v=5Y2EiZST97Y", "blind75": False},
    {"title": "Add Two Numbers", "diff": "Medium", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/add-two-numbers/", "yt": "https://www.youtube.com/watch?v=wgFPrzTjm7s", "blind75": False},
    {"title": "Linked List Cycle", "diff": "Easy", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/linked-list-cycle/", "yt": "https://www.youtube.com/watch?v=gBTe7lFR3vc", "blind75": True},
    {"title": "Find the Duplicate Number", "diff": "Medium", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/find-the-duplicate-number/", "yt": "https://www.youtube.com/watch?v=wjYnzkAhcNk", "blind75": False},
    {"title": "LRU Cache", "diff": "Medium", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/lru-cache/", "yt": "https://www.youtube.com/watch?v=7ABFKPK2hD4", "blind75": False},
    {"title": "Merge k Sorted Lists", "diff": "Hard", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/merge-k-sorted-lists/", "yt": "https://www.youtube.com/watch?v=q5a5OiGbT6Q", "blind75": True},
    {"title": "Reverse Nodes in k-Group", "diff": "Hard", "step": "step-6", "subtopic": "⚡ NeetCode 150: Linked List Patterns", "lc": "https://leetcode.com/problems/reverse-nodes-in-k-group/", "yt": "https://www.youtube.com/watch?v=1UOPsfP85V4", "blind75": False},

    # Trees
    {"title": "Invert Binary Tree", "diff": "Easy", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/invert-binary-tree/", "yt": "https://www.youtube.com/watch?v=OnSn2XEQ4MY", "blind75": True},
    {"title": "Maximum Depth of Binary Tree", "diff": "Easy", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/maximum-depth-of-binary-tree/", "yt": "https://www.youtube.com/watch?v=hTM3phJS6GE", "blind75": True},
    {"title": "Diameter of Binary Tree", "diff": "Easy", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/diameter-of-binary-tree/", "yt": "https://www.youtube.com/watch?v=bkxqA8Rfo04", "blind75": False},
    {"title": "Balanced Binary Tree", "diff": "Easy", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/balanced-binary-tree/", "yt": "https://www.youtube.com/watch?v=QfJsau0ItOY", "blind75": False},
    {"title": "Same Tree", "diff": "Easy", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/same-tree/", "yt": "https://www.youtube.com/watch?v=vRbbcKXCxOw", "blind75": True},
    {"title": "Subtree of Another Tree", "diff": "Easy", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/subtree-of-another-tree/", "yt": "https://www.youtube.com/watch?v=E36O5SWp-LE", "blind75": True},
    {"title": "Lowest Common Ancestor of a Binary Search Tree", "diff": "Medium", "step": "step-14", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/", "yt": "https://www.youtube.com/watch?v=gs2LMfuOR9k", "blind75": True},
    {"title": "Binary Tree Level Order Traversal", "diff": "Medium", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/binary-tree-level-order-traversal/", "yt": "https://www.youtube.com/watch?v=6ZnyEApgFYg", "blind75": True},
    {"title": "Binary Tree Right Side View", "diff": "Medium", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/binary-tree-right-side-view/", "yt": "https://www.youtube.com/watch?v=d4zLyf32TnQ", "blind75": False},
    {"title": "Count Good Nodes in Binary Tree", "diff": "Medium", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/count-good-nodes-in-binary-tree/", "yt": "https://www.youtube.com/watch?v=7cp5imvDzl4", "blind75": False},
    {"title": "Validate Binary Search Tree", "diff": "Medium", "step": "step-14", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/validate-binary-search-tree/", "yt": "https://www.youtube.com/watch?v=s6ATEkipzow", "blind75": True},
    {"title": "Kth Smallest Element in a BST", "diff": "Medium", "step": "step-14", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/", "yt": "https://www.youtube.com/watch?v=5LUXSv742kg", "blind75": True},
    {"title": "Construct Binary Tree from Preorder and Inorder Traversal", "diff": "Medium", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/", "yt": "https://www.youtube.com/watch?v=ihj4IQGZ2zc", "blind75": True},
    {"title": "Binary Tree Maximum Path Sum", "diff": "Hard", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/binary-tree-maximum-path-sum/", "yt": "https://www.youtube.com/watch?v=Hr5cWUld4vU", "blind75": True},
    {"title": "Serialize and Deserialize Binary Tree", "diff": "Hard", "step": "step-13", "subtopic": "⚡ NeetCode 150: Tree Patterns", "lc": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/", "yt": "https://www.youtube.com/watch?v=u4JAi2JJhIg", "blind75": True},

    # Tries
    {"title": "Implement Trie (Prefix Tree)", "diff": "Medium", "step": "step-17", "subtopic": "⚡ NeetCode 150: Trie Patterns", "lc": "https://leetcode.com/problems/implement-trie-prefix-tree/", "yt": "https://www.youtube.com/watch?v=oobqoCJlHA0", "blind75": True},
    {"title": "Design Add and Search Words Data Structure", "diff": "Medium", "step": "step-17", "subtopic": "⚡ NeetCode 150: Trie Patterns", "lc": "https://leetcode.com/problems/design-add-and-search-words-data-structure/", "yt": "https://www.youtube.com/watch?v=BTf05gs_8iU", "blind75": True},
    {"title": "Word Search II", "diff": "Hard", "step": "step-17", "subtopic": "⚡ NeetCode 150: Trie Patterns", "lc": "https://leetcode.com/problems/word-search-ii/", "yt": "https://www.youtube.com/watch?v=asbcE9mZz_U", "blind75": True},

    # Heap / Priority Queue
    {"title": "Kth Largest Element in a Stream", "diff": "Easy", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/kth-largest-element-in-a-stream/", "yt": "https://www.youtube.com/watch?v=hOjcdrqMoQ8", "blind75": False},
    {"title": "Last Stone Weight", "diff": "Easy", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/last-stone-weight/", "yt": "https://www.youtube.com/watch?v=B-QCq79-Vfw", "blind75": False},
    {"title": "K Closest Points to Origin", "diff": "Medium", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/k-closest-points-to-origin/", "yt": "https://www.youtube.com/watch?v=rI2EBUEMfTk", "blind75": False},
    {"title": "Kth Largest Element in an Array", "diff": "Medium", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/kth-largest-element-in-an-array/", "yt": "https://www.youtube.com/watch?v=XEmy13g1Qxc", "blind75": False},
    {"title": "Task Scheduler", "diff": "Medium", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/task-scheduler/", "yt": "https://www.youtube.com/watch?v=s8p8ukTyA2I", "blind75": False},
    {"title": "Design Twitter", "diff": "Medium", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/design-twitter/", "yt": "https://www.youtube.com/watch?v=pNichitDD2E", "blind75": False},
    {"title": "Find Median from Data Stream", "diff": "Hard", "step": "step-11", "subtopic": "⚡ NeetCode 150: Heap & Priority Queue Patterns", "lc": "https://leetcode.com/problems/find-median-from-data-stream/", "yt": "https://www.youtube.com/watch?v=itmhHWaHupI", "blind75": True},

    # Backtracking
    {"title": "Subsets", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/subsets/", "yt": "https://www.youtube.com/watch?v=REOH22XwdVM", "blind75": False},
    {"title": "Combination Sum", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/combination-sum/", "yt": "https://www.youtube.com/watch?v=GBKI9VSKdGg", "blind75": True},
    {"title": "Permutations", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/permutations/", "yt": "https://www.youtube.com/watch?v=s7AvT7cGdSo", "blind75": False},
    {"title": "Subsets II", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/subsets-ii/", "yt": "https://www.youtube.com/watch?v=Vn2v6ajA7U0", "blind75": False},
    {"title": "Combination Sum II", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/combination-sum-ii/", "yt": "https://www.youtube.com/watch?v=rSA3t6BDDwg", "blind75": False},
    {"title": "Word Search", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/word-search/", "yt": "https://www.youtube.com/watch?v=pfiQ_PS1g8E", "blind75": True},
    {"title": "Palindrome Partitioning", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/palindrome-partitioning/", "yt": "https://www.youtube.com/watch?v=3jvWodd7ht0", "blind75": False},
    {"title": "Letter Combinations of a Phone Number", "diff": "Medium", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/", "yt": "https://www.youtube.com/watch?v=0snEunUacZY", "blind75": False},
    {"title": "N-Queens", "diff": "Hard", "step": "step-7", "subtopic": "⚡ NeetCode 150: Backtracking Patterns", "lc": "https://leetcode.com/problems/n-queens/", "yt": "https://www.youtube.com/watch?v=Ph95IHmRp5M", "blind75": False},

    # Graphs
    {"title": "Number of Islands", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/number-of-islands/", "yt": "https://www.youtube.com/watch?v=pV2kpPD66nE", "blind75": True},
    {"title": "Clone Graph", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/clone-graph/", "yt": "https://www.youtube.com/watch?v=mQeF6bN8hMk", "blind75": True},
    {"title": "Max Area of Island", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/max-area-of-island/", "yt": "https://www.youtube.com/watch?v=iJGr1OtmH0c", "blind75": False},
    {"title": "Pacific Atlantic Water Flow", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/pacific-atlantic-water-flow/", "yt": "https://www.youtube.com/watch?v=s-AngeVwgP8", "blind75": True},
    {"title": "Surrounded Regions", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/surrounded-regions/", "yt": "https://www.youtube.com/watch?v=9z2BunfoZ5Y", "blind75": False},
    {"title": "Rotting Oranges", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/rotting-oranges/", "yt": "https://www.youtube.com/watch?v=y704fEOx0i0", "blind75": False},
    {"title": "Course Schedule", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/course-schedule/", "yt": "https://www.youtube.com/watch?v=EgI5nU9etnU", "blind75": True},
    {"title": "Course Schedule II", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/course-schedule-ii/", "yt": "https://www.youtube.com/watch?v=Akt3glAwyfY", "blind75": False},
    {"title": "Redundant Connection", "diff": "Medium", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/redundant-connection/", "yt": "https://www.youtube.com/watch?v=FXWRE67PLL0", "blind75": False},
    {"title": "Word Ladder", "diff": "Hard", "step": "step-15", "subtopic": "⚡ NeetCode 150: Graph Patterns", "lc": "https://leetcode.com/problems/word-ladder/", "yt": "https://www.youtube.com/watch?v=h9iTnkgv05E", "blind75": True},

    # 1-D Dynamic Programming
    {"title": "Climbing Stairs", "diff": "Easy", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/climbing-stairs/", "yt": "https://www.youtube.com/watch?v=Y0lT9Fck7qI", "blind75": True},
    {"title": "Min Cost Climbing Stairs", "diff": "Easy", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/min-cost-climbing-stairs/", "yt": "https://www.youtube.com/watch?v=ktmzAZWkEZ0", "blind75": False},
    {"title": "House Robber", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/house-robber/", "yt": "https://www.youtube.com/watch?v=73r3KWiEvyk", "blind75": True},
    {"title": "House Robber II", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/house-robber-ii/", "yt": "https://www.youtube.com/watch?v=rWAJCfYYOvM", "blind75": True},
    {"title": "Longest Palindromic Substring", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/longest-palindromic-substring/", "yt": "https://www.youtube.com/watch?v=XYQecbcd6_c", "blind75": True},
    {"title": "Palindromic Substrings", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/palindromic-substrings/", "yt": "https://www.youtube.com/watch?v=4RACzI5-du8", "blind75": True},
    {"title": "Decode Ways", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/decode-ways/", "yt": "https://www.youtube.com/watch?v=6aEyTjOwlJU", "blind75": True},
    {"title": "Coin Change", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/coin-change/", "yt": "https://www.youtube.com/watch?v=H9bfqozjoqs", "blind75": True},
    {"title": "Maximum Product Subarray", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/maximum-product-subarray/", "yt": "https://www.youtube.com/watch?v=lXVy6YWFcRM", "blind75": True},
    {"title": "Word Break", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/word-break/", "yt": "https://www.youtube.com/watch?v=Sx9NNgInc3A", "blind75": True},
    {"title": "Longest Increasing Subsequence", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/longest-increasing-subsequence/", "yt": "https://www.youtube.com/watch?v=cjWnW0hdF1Y", "blind75": True},
    {"title": "Partition Equal Subset Sum", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 1-D DP Patterns", "lc": "https://leetcode.com/problems/partition-equal-subset-sum/", "yt": "https://www.youtube.com/watch?v=IsvocB5BJhw", "blind75": False},

    # 2-D Dynamic Programming
    {"title": "Unique Paths", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 2-D DP Patterns", "lc": "https://leetcode.com/problems/unique-paths/", "yt": "https://www.youtube.com/watch?v=IlEsdxuD4lY", "blind75": True},
    {"title": "Longest Common Subsequence", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 2-D DP Patterns", "lc": "https://leetcode.com/problems/longest-common-subsequence/", "yt": "https://www.youtube.com/watch?v=Ua0GhsJSlWM", "blind75": True},
    {"title": "Best Time to Buy and Sell Stock with Cooldown", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 2-D DP Patterns", "lc": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/", "yt": "https://www.youtube.com/watch?v=I7j0F7AHpb8", "blind75": False},
    {"title": "Coin Change II", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 2-D DP Patterns", "lc": "https://leetcode.com/problems/coin-change-ii/", "yt": "https://www.youtube.com/watch?v=Mjy4hd2xgrs", "blind75": False},
    {"title": "Target Sum", "diff": "Medium", "step": "step-16", "subtopic": "⚡ NeetCode 150: 2-D DP Patterns", "lc": "https://leetcode.com/problems/target-sum/", "yt": "https://www.youtube.com/watch?v=g0npyaQtAQM", "blind75": False},
    {"title": "Edit Distance", "diff": "Hard", "step": "step-16", "subtopic": "⚡ NeetCode 150: 2-D DP Patterns", "lc": "https://leetcode.com/problems/edit-distance/", "yt": "https://www.youtube.com/watch?v=XYi2-LPrwm4", "blind75": False},

    # Greedy
    {"title": "Maximum Subarray", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Greedy Patterns", "lc": "https://leetcode.com/problems/maximum-subarray/", "yt": "https://www.youtube.com/watch?v=5WZl3MMT0Eg", "blind75": True},
    {"title": "Jump Game", "diff": "Medium", "step": "step-12", "subtopic": "⚡ NeetCode 150: Greedy Patterns", "lc": "https://leetcode.com/problems/jump-game/", "yt": "https://www.youtube.com/watch?v=Yan0cv2cLy8", "blind75": True},
    {"title": "Jump Game II", "diff": "Medium", "step": "step-12", "subtopic": "⚡ NeetCode 150: Greedy Patterns", "lc": "https://leetcode.com/problems/jump-game-ii/", "yt": "https://www.youtube.com/watch?v=dJ7sWiOoK7g", "blind75": False},
    {"title": "Gas Station", "diff": "Medium", "step": "step-12", "subtopic": "⚡ NeetCode 150: Greedy Patterns", "lc": "https://leetcode.com/problems/gas-station/", "yt": "https://www.youtube.com/watch?v=lJwbPZGo05A", "blind75": False},

    # Intervals
    {"title": "Insert Interval", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Interval Patterns", "lc": "https://leetcode.com/problems/insert-interval/", "yt": "https://www.youtube.com/watch?v=dxb_6t9uV_s", "blind75": True},
    {"title": "Merge Intervals", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Interval Patterns", "lc": "https://leetcode.com/problems/merge-intervals/", "yt": "https://www.youtube.com/watch?v=44H3cEC2fFM", "blind75": True},
    {"title": "Non-overlapping Intervals", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Interval Patterns", "lc": "https://leetcode.com/problems/non-overlapping-intervals/", "yt": "https://www.youtube.com/watch?v=nONCGxWoUfM", "blind75": True},
    {"title": "Meeting Rooms", "diff": "Easy", "step": "step-3", "subtopic": "⚡ NeetCode 150: Interval Patterns", "lc": "https://leetcode.com/problems/meeting-rooms/", "yt": "https://www.youtube.com/watch?v=PaJxqte9610", "blind75": True},
    {"title": "Meeting Rooms II", "diff": "Medium", "step": "step-3", "subtopic": "⚡ NeetCode 150: Interval Patterns", "lc": "https://leetcode.com/problems/meeting-rooms-ii/", "yt": "https://www.youtube.com/watch?v=FdzJmTCVyJU", "blind75": True},

    # Bit Manipulation
    {"title": "Single Number", "diff": "Easy", "step": "step-8", "subtopic": "⚡ NeetCode 150: Bit Manipulation Patterns", "lc": "https://leetcode.com/problems/single-number/", "yt": "https://www.youtube.com/watch?v=qMPX1AOa83k", "blind75": True},
    {"title": "Number of 1 Bits", "diff": "Easy", "step": "step-8", "subtopic": "⚡ NeetCode 150: Bit Manipulation Patterns", "lc": "https://leetcode.com/problems/number-of-1-bits/", "yt": "https://www.youtube.com/watch?v=5Km3utixwZs", "blind75": True},
    {"title": "Counting Bits", "diff": "Easy", "step": "step-8", "subtopic": "⚡ NeetCode 150: Bit Manipulation Patterns", "lc": "https://leetcode.com/problems/counting-bits/", "yt": "https://www.youtube.com/watch?v=RyBM56P6mt8", "blind75": True},
    {"title": "Reverse Bits", "diff": "Easy", "step": "step-8", "subtopic": "⚡ NeetCode 150: Bit Manipulation Patterns", "lc": "https://leetcode.com/problems/reverse-bits/", "yt": "https://www.youtube.com/watch?v=UcoN6UjAI64", "blind75": True},
    {"title": "Missing Number", "diff": "Easy", "step": "step-8", "subtopic": "⚡ NeetCode 150: Bit Manipulation Patterns", "lc": "https://leetcode.com/problems/missing-number/", "yt": "https://www.youtube.com/watch?v=WnPLSRLSANE", "blind75": True},
    {"title": "Sum of Two Integers", "diff": "Medium", "step": "step-8", "subtopic": "⚡ NeetCode 150: Bit Manipulation Patterns", "lc": "https://leetcode.com/problems/sum-of-two-integers/", "yt": "https://www.youtube.com/watch?v=gVUrDV4tZfY", "blind75": True}
]

# Step 1: Match existing problems and tag with isNeetCode and isBlind75
matched_count = 0
for step in data:
    for topic in step['topics']:
        for prob in topic['problems']:
            p_title = prob['title'].lower()
            for nc in neetcode_150_dataset:
                nc_title = nc['title'].lower()
                if nc_title in p_title or p_title in nc_title or (prob.get('leetcode') and nc['lc'] and prob['leetcode'] == nc['lc']):
                    prob['isNeetCode'] = True
                    if nc['blind75']:
                        prob['isBlind75'] = True
                    if nc['yt']:
                        prob['neetcode'] = nc['yt']
                    matched_count += 1
                    break

print(f"Matched and tagged {matched_count} existing problems with NeetCode 150 & Blind 75 badges!")

# Step 2: Check if any NeetCode problem is completely missing, and append it cleanly to its matching step
next_id = max_id + 1
appended_count = 0

step_map = {s['stepId']: s for s in data}

# Group missing by step and subtopic
for nc in neetcode_150_dataset:
    # Check if this title is in data
    found = False
    for step in data:
        for topic in step['topics']:
            for prob in topic['problems']:
                if nc['title'].lower() in prob['title'].lower() or (prob.get('leetcode') and nc['lc'] and prob['leetcode'] == nc['lc']):
                    found = True
                    break
            if found:
                break
        if found:
            break

    if not found and nc['step'] in step_map:
        target_step = step_map[nc['step']]
        # Find or create subtopic
        target_topic = None
        for t in target_step['topics']:
            if t['subtopic'] == nc['subtopic']:
                target_topic = t
                break
        if not target_topic:
            target_topic = {"subtopic": nc['subtopic'], "problems": []}
            target_step['topics'].append(target_topic)

        target_topic['problems'].append({
            "id": next_id,
            "title": nc['title'],
            "difficulty": nc['diff'],
            "link": nc['lc'],
            "article": "https://neetcode.io/practice",
            "youtube": nc['yt'],
            "neetcode": nc['yt'],
            "leetcode": nc['lc'],
            "isNeetCode": True,
            "isBlind75": nc['blind75']
        })
        next_id += 1
        appended_count += 1

print(f"Appended {appended_count} distinct NeetCode 150 problems into your steps!")

# Save to data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet + Unified NeetCode 150 & Blind 75 Pattern Base\n")
    f.write("const DSA_DATA = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

total = sum(len(t['problems']) for s in data for t in s['topics'])
print(f"New Grand Total Problems in Vault: {total}")
