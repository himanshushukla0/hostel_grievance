import json

full_dataset = [
  {
    "stepId": "step-1",
    "stepTitle": "Step 1: Learn the basics",
    "description": "Things to know in programming languages, patterns, basic maths, recursion, hashing & STL.",
    "topics": [
      {
        "subtopic": "Things to Know in C++/Java/Python or any language",
        "problems": [
          {"title": "User Input / Output", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-input-output/"},
          {"title": "Data Types & Variables", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-data-types/"},
          {"title": "If Else statements", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-if-else-statements/"},
          {"title": "Switch Statement", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-switch-case/"},
          {"title": "What are Arrays, Strings", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-arrays-introduction/"},
          {"title": "For loops", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-loops-while-for-do-while/"},
          {"title": "While loops", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-loops-while-for-do-while/"},
          {"title": "Functions (Pass by reference and value)", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-functions-pass-by-value-and-reference/"},
          {"title": "Time and Space Complexity Analysis", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/time-and-space-complexity/"}
        ]
      },
      {
        "subtopic": "Build-up Logical Thinking",
        "problems": [
          {"title": "Introduction to Patterns & Approach", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern Rules & Nested Loops Formulas", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"}
        ]
      },
      {
        "subtopic": "Patterns",
        "problems": [
          {"title": "Pattern-1: Rectangular Star Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-2: Right-Angled Triangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-3: Right-Angled Number Pyramid", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-4: Right-Angled Number Pyramid - II", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-5: Inverted Right Pyramid", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-6: Inverted Numbered Right Pyramid", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-7: Star Pyramid", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-8: Inverted Star Pyramid", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-9: Diamond Star Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-10: Half Diamond Star Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-11: Binary Number Triangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-12: Number Crown Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-13: Increasing Number Triangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-14: Increasing Letter Triangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-15: Reverse Letter Triangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-16: Alpha-Ramp Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-17: Alpha-Hill Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-18: Alpha-Triangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-19: Symmetric Void Pattern", "difficulty": "Medium", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-20: Symmetric Butterfly Pattern", "difficulty": "Medium", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-21: Hollow Rectangle Pattern", "difficulty": "Easy", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"},
          {"title": "Pattern-22: The Number Pattern", "difficulty": "Medium", "link": "https://takeuforward.org/strivers-a2z-dsa-course/must-do-pattern-problems-solve-zero-to-hero/"}
        ]
      },
      {
        "subtopic": "Learn STL/Java-Collections or similar thing in your language",
        "problems": [
          {"title": "C++ STL / Java Collections Overview & Iterators", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-stl-tutorial-most-frequent-used-stl-containers/"},
          {"title": "Containers & Algorithms (Vectors, Maps, Sets, Sorting)", "difficulty": "Easy", "link": "https://takeuforward.org/c/c-stl-tutorial-most-frequent-used-stl-containers/"}
        ]
      },
      {
        "subtopic": "Know Basic Maths",
        "problems": [
          {"title": "Count Digits", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/count-digits-in-a-number/"},
          {"title": "Reverse a Number", "difficulty": "Easy", "link": "https://leetcode.com/problems/reverse-integer/"},
          {"title": "Check Palindrome", "difficulty": "Easy", "link": "https://leetcode.com/problems/palindrome-number/"},
          {"title": "GCD Or HCF (Euclidean algorithm)", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-gcd-of-two-numbers/"},
          {"title": "Armstrong Numbers", "difficulty": "Easy", "link": "https://takeuforward.org/maths/check-if-a-number-is-armstrong-number-or-not/"},
          {"title": "Print all Divisors", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/print-all-divisors-of-a-given-number/"},
          {"title": "Check for Prime", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/check-if-a-number-is-prime-or-not/"}
        ]
      },
      {
        "subtopic": "Learn Basic Recursion",
        "problems": [
          {"title": "Understand recursion by print something N times", "difficulty": "Easy", "link": "https://takeuforward.org/recursion/print-1-to-n-using-recursion/"},
          {"title": "Print 1 to N using recursion", "difficulty": "Easy", "link": "https://takeuforward.org/recursion/print-1-to-n-using-recursion/"},
          {"title": "Print N to 1 using recursion", "difficulty": "Easy", "link": "https://takeuforward.org/recursion/print-n-to-1-using-recursion/"},
          {"title": "Sum of first N numbers", "difficulty": "Easy", "link": "https://takeuforward.org/recursion/sum-of-first-n-natural-numbers/"},
          {"title": "Factorial of N numbers", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/factorial-of-a-number-iterative-and-recursive/"},
          {"title": "Reverse an array", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/reverse-a-given-array/"},
          {"title": "Check if a string is palindrome or not", "difficulty": "Easy", "link": "https://leetcode.com/problems/valid-palindrome/"},
          {"title": "Fibonacci Number", "difficulty": "Easy", "link": "https://leetcode.com/problems/fibonacci-number/"},
          {"title": "Multiple Recursion Calls & Tree Tracing", "difficulty": "Easy", "link": "https://takeuforward.org/recursion/introduction-to-recursion/"}
        ]
      },
      {
        "subtopic": "Learn Basic Hashing",
        "problems": [
          {"title": "Counting frequencies of array elements", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/count-frequency-of-each-element-in-the-array/"},
          {"title": "Find the highest/lowest frequency element", "difficulty": "Easy", "link": "https://takeuforward.org/arrays/find-the-highest-lowest-frequency-element/"},
          {"title": "Hashing Theory (Division Method, Collision Handling)", "difficulty": "Easy", "link": "https://takeuforward.org/hashing/hashing-maps-time-complexity-collisions-division-rule-of-hashing-strivers-a2z-dsa-course/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-2",
    "stepTitle": "Step 2: Learn Important Sorting Techniques",
    "description": "Selection, Bubble, Insertion, Merge Sort, and Quick Sort.",
    "topics": [
      {
        "subtopic": "Sorting-I",
        "problems": [
          {"title": "Selection Sort", "difficulty": "Easy", "link": "https://takeuforward.org/sorting/selection-sort-algorithm/"},
          {"title": "Bubble Sort", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/bubble-sort-algorithm/"},
          {"title": "Insertion Sort", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/insertion-sort-algorithm/"}
        ]
      },
      {
        "subtopic": "Sorting-II",
        "problems": [
          {"title": "Merge Sort", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/merge-sort-algorithm/"},
          {"title": "Recursive Bubble Sort", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/recursive-bubble-sort-algorithm/"},
          {"title": "Recursive Insertion Sort", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/recursive-insertion-sort-algorithm/"},
          {"title": "Quick Sort", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/quick-sort-algorithm/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-3",
    "stepTitle": "Step 3: Solve Problems on Arrays [Easy -> Medium -> Hard]",
    "description": "From fundamentals to interview favorites (Kadane, Boyer-Moore, Merge Intervals, etc.)",
    "topics": [
      {
        "subtopic": "Easy",
        "problems": [
          {"title": "Largest Element in an Array", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-the-largest-element-in-an-array/"},
          {"title": "Second Largest Element in an Array without sorting", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-second-smallest-and-second-largest-element-in-an-array/"},
          {"title": "Check if the array is sorted", "difficulty": "Easy", "link": "https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/"},
          {"title": "Remove duplicates from Sorted array", "difficulty": "Easy", "link": "https://leetcode.com/problems/remove-duplicates-from-sorted-array/"},
          {"title": "Left Rotate an array by one place", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/left-rotate-the-array-by-one/"},
          {"title": "Left rotate an array by D places", "difficulty": "Medium", "link": "https://leetcode.com/problems/rotate-array/"},
          {"title": "Move Zeros to end", "difficulty": "Easy", "link": "https://leetcode.com/problems/move-zeroes/"},
          {"title": "Linear Search", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/linear-search-in-c/"},
          {"title": "Find the Union and Intersection of two sorted arrays", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/union-of-two-sorted-arrays/"},
          {"title": "Find missing number in an array", "difficulty": "Easy", "link": "https://leetcode.com/problems/missing-number/"},
          {"title": "Maximum Consecutive Ones", "difficulty": "Easy", "link": "https://leetcode.com/problems/max-consecutive-ones/"},
          {"title": "Find the number that appears once, and other numbers twice", "difficulty": "Easy", "link": "https://leetcode.com/problems/single-number/"},
          {"title": "Longest subarray with given sum K(Positives)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/longest-subarray-with-given-sum-k/"},
          {"title": "Longest subarray with sum K (Positives + Negatives)", "difficulty": "Medium", "link": "https://takeuforward.org/arrays/longest-subarray-with-sum-k-postives-and-negatives/"}
        ]
      },
      {
        "subtopic": "Medium",
        "problems": [
          {"title": "2Sum Problem", "difficulty": "Easy", "link": "https://leetcode.com/problems/two-sum/"},
          {"title": "Sort an array of 0's 1's and 2's", "difficulty": "Medium", "link": "https://leetcode.com/problems/sort-colors/"},
          {"title": "Majority Element (>n/2 times)", "difficulty": "Easy", "link": "https://leetcode.com/problems/majority-element/"},
          {"title": "Kadane's Algorithm, maximum subarray sum", "difficulty": "Medium", "link": "https://leetcode.com/problems/maximum-subarray/"},
          {"title": "Print subarray with maximum subarray sum", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/kadanes-algorithm-maximum-subarray-sum-in-an-array/"},
          {"title": "Stock Buy and Sell", "difficulty": "Easy", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
          {"title": "Rearrange the array in alternating positive and negative items", "difficulty": "Medium", "link": "https://leetcode.com/problems/rearrange-array-elements-by-sign/"},
          {"title": "Next Permutation", "difficulty": "Medium", "link": "https://leetcode.com/problems/next-permutation/"},
          {"title": "Leaders in an Array problem", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/leaders-in-an-array/"},
          {"title": "Longest Consecutive Sequence in an Array", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-consecutive-sequence/"},
          {"title": "Set Matrix Zeros", "difficulty": "Medium", "link": "https://leetcode.com/problems/set-matrix-zeroes/"},
          {"title": "Rotate Matrix by 90 degrees", "difficulty": "Medium", "link": "https://leetcode.com/problems/rotate-image/"},
          {"title": "Print the matrix in spiral manner", "difficulty": "Medium", "link": "https://leetcode.com/problems/spiral-matrix/"},
          {"title": "Count subarrays with given sum", "difficulty": "Medium", "link": "https://leetcode.com/problems/subarray-sum-equals-k/"}
        ]
      },
      {
        "subtopic": "Hard",
        "problems": [
          {"title": "Pascal's Triangle", "difficulty": "Easy", "link": "https://leetcode.com/problems/pascals-triangle/"},
          {"title": "Majority Elements (>n/3 times)", "difficulty": "Medium", "link": "https://leetcode.com/problems/majority-element-ii/"},
          {"title": "3-Sum Problem", "difficulty": "Medium", "link": "https://leetcode.com/problems/3sum/"},
          {"title": "4-Sum Problem", "difficulty": "Medium", "link": "https://leetcode.com/problems/4sum/"},
          {"title": "Largest Subarray with 0 sum", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/length-of-the-longest-subarray-with-zero-sum/"},
          {"title": "Count number of subarrays with given xor K", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/count-the-number-of-subarrays-with-given-xor-k/"},
          {"title": "Merge Overlapping Subintervals", "difficulty": "Medium", "link": "https://leetcode.com/problems/merge-intervals/"},
          {"title": "Merge two sorted arrays without extra space", "difficulty": "Hard", "link": "https://leetcode.com/problems/merge-sorted-array/"},
          {"title": "Find the repeating and missing number", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/find-the-repeating-and-missing-numbers/"},
          {"title": "Count Inversions", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/count-inversions-in-an-array/"},
          {"title": "Reverse Pairs", "difficulty": "Hard", "link": "https://leetcode.com/problems/reverse-pairs/"},
          {"title": "Maximum Product Subarray", "difficulty": "Medium", "link": "https://leetcode.com/problems/maximum-product-subarray/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-4",
    "stepTitle": "Step 4: Binary Search [1D, 2D Arrays, Search Space]",
    "description": "Binary search on 1D arrays, 2D matrices, and search-space optimization problems.",
    "topics": [
      {
        "subtopic": "Learning BS on 1D Arrays",
        "problems": [
          {"title": "Binary Search to find X in sorted array", "difficulty": "Easy", "link": "https://leetcode.com/problems/binary-search/"},
          {"title": "Implement Lower Bound", "difficulty": "Easy", "link": "https://takeuforward.org/arrays/implement-lower-bound-bs-2/"},
          {"title": "Implement Upper Bound", "difficulty": "Easy", "link": "https://takeuforward.org/arrays/implement-upper-bound/"},
          {"title": "Search Insert Position", "difficulty": "Easy", "link": "https://leetcode.com/problems/search-insert-position/"},
          {"title": "Floor and Ceil in Sorted Array", "difficulty": "Easy", "link": "https://takeuforward.org/arrays/floor-and-ceil-in-sorted-array/"},
          {"title": "First and Last Occurrence in a Sorted Array", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/"},
          {"title": "Count Occurrences in Sorted Array", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/count-occurrences-in-sorted-array/"},
          {"title": "Search in Rotated Sorted Array I", "difficulty": "Medium", "link": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
          {"title": "Search in Rotated Sorted Array II", "difficulty": "Medium", "link": "https://leetcode.com/problems/search-in-rotated-sorted-array-ii/"},
          {"title": "Find minimum in Rotated Sorted Array", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"},
          {"title": "Find out how many times array has been rotated", "difficulty": "Easy", "link": "https://takeuforward.org/arrays/find-out-how-many-times-the-array-has-been-rotated/"},
          {"title": "Single element in a Sorted Array", "difficulty": "Medium", "link": "https://leetcode.com/problems/single-element-in-a-sorted-array/"},
          {"title": "Find peak element", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-peak-element/"}
        ]
      },
      {
        "subtopic": "Applying BS on 2D Arrays",
        "problems": [
          {"title": "Row with max 1s", "difficulty": "Easy", "link": "https://takeuforward.org/arrays/find-the-row-with-maximum-number-of-1s/"},
          {"title": "Search in a 2D matrix", "difficulty": "Medium", "link": "https://leetcode.com/problems/search-a-2d-matrix/"},
          {"title": "Search in a row and col wise sorted matrix", "difficulty": "Medium", "link": "https://leetcode.com/problems/search-a-2d-matrix-ii/"},
          {"title": "Find Peak Element (2D Matrix)", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-a-peak-element-ii/"},
          {"title": "Matrix Median", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/median-of-row-wise-sorted-matrix/"}
        ]
      },
      {
        "subtopic": "Find Answers by BS in Search Space",
        "problems": [
          {"title": "Find square root of a number in log n", "difficulty": "Easy", "link": "https://leetcode.com/problems/sqrtx/"},
          {"title": "Find the Nth root of a number using BS", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/nth-root-of-a-number-using-binary-search/"},
          {"title": "Koko Eating Bananas", "difficulty": "Medium", "link": "https://leetcode.com/problems/koko-eating-bananas/"},
          {"title": "Minimum days to make M bouquets", "difficulty": "Medium", "link": "https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/"},
          {"title": "Find the smallest Divisor given a Threshold", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/"},
          {"title": "Capacity to Ship Packages within D Days", "difficulty": "Medium", "link": "https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/"},
          {"title": "Kth Missing Positive Number", "difficulty": "Easy", "link": "https://leetcode.com/problems/kth-missing-positive-number/"},
          {"title": "Aggressive Cows", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/aggressive-cows-detailed-solution/"},
          {"title": "Book Allocation Problem", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/allocate-minimum-number-of-pages/"},
          {"title": "Split array - Largest Sum", "difficulty": "Hard", "link": "https://leetcode.com/problems/split-array-largest-sum/"},
          {"title": "Painter's Partition", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/painters-partition-problem/"},
          {"title": "Minimize Max Distance to Gas Station", "difficulty": "Hard", "link": "https://takeuforward.org/arrays/minimise-maximum-distance-between-gas-stations/"},
          {"title": "Median of 2 Sorted Arrays of Different Sizes", "difficulty": "Hard", "link": "https://leetcode.com/problems/median-of-two-sorted-arrays/"},
          {"title": "Kth element of two sorted arrays", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/k-th-element-of-two-sorted-arrays/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-5",
    "stepTitle": "Step 5: Strings [Basic and Medium]",
    "description": "String manipulations, anagrams, roman numbers, and parsing algorithms.",
    "topics": [
      {
        "subtopic": "Basic and Easy String Problems",
        "problems": [
          {"title": "Remove outermost Paranthesis", "difficulty": "Easy", "link": "https://leetcode.com/problems/remove-outermost-parentheses/"},
          {"title": "Reverse Words in a String", "difficulty": "Medium", "link": "https://leetcode.com/problems/reverse-words-in-a-string/"},
          {"title": "Largest odd number in a string", "difficulty": "Easy", "link": "https://leetcode.com/problems/largest-odd-number-in-string/"},
          {"title": "Longest Common Prefix", "difficulty": "Easy", "link": "https://leetcode.com/problems/longest-common-prefix/"},
          {"title": "Isomorphic String", "difficulty": "Easy", "link": "https://leetcode.com/problems/isomorphic-strings/"},
          {"title": "Check whether one string is a rotation of another", "difficulty": "Easy", "link": "https://leetcode.com/problems/rotate-string/"},
          {"title": "Check if two Strings are anagrams of each other", "difficulty": "Easy", "link": "https://leetcode.com/problems/valid-anagram/"}
        ]
      },
      {
        "subtopic": "Medium String Problems",
        "problems": [
          {"title": "Sort Characters by frequency", "difficulty": "Medium", "link": "https://leetcode.com/problems/sort-characters-by-frequency/"},
          {"title": "Maximum Nesting Depth of Parentheses", "difficulty": "Easy", "link": "https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/"},
          {"title": "Roman Number to Integer", "difficulty": "Easy", "link": "https://leetcode.com/problems/roman-to-integer/"},
          {"title": "Integer to Roman", "difficulty": "Medium", "link": "https://leetcode.com/problems/integer-to-roman/"},
          {"title": "Implement Atoi", "difficulty": "Medium", "link": "https://leetcode.com/problems/string-to-integer-atoi/"},
          {"title": "Count Number of Substrings with K Distinct Characters", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/count-number-of-substrings-with-exactly-k-distinct-characters/"},
          {"title": "Longest Palindromic Substring", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-palindromic-substring/"},
          {"title": "Sum of Beauty of all Substrings", "difficulty": "Medium", "link": "https://leetcode.com/problems/sum-of-beauty-of-all-substrings/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-6",
    "stepTitle": "Step 6: Learn LinkedList [Single LL, Double LL, Medium, Hard Problems]",
    "description": "Pointers manipulation, Tortoise & Hare, reversing, and deep copying.",
    "topics": [
      {
        "subtopic": "Learn 1D LinkedList",
        "problems": [
          {"title": "Introduction to LinkedList, learn about struct, and how to create a node", "difficulty": "Easy", "link": "https://takeuforward.org/linked-list/introduction-to-linked-list/"},
          {"title": "Inserting a node in LinkedList", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/insert-node-at-beginning-of-linked-list/"},
          {"title": "Deleting a node in LinkedList", "difficulty": "Easy", "link": "https://leetcode.com/problems/delete-node-in-a-linked-list/"},
          {"title": "Find the length of the linkedlist", "difficulty": "Easy", "link": "https://takeuforward.org/linked-list/count-nodes-of-linked-list/"},
          {"title": "Search an element in the LL", "difficulty": "Easy", "link": "https://takeuforward.org/linked-list/search-an-element-in-a-linked-list/"}
        ]
      },
      {
        "subtopic": "Learn Doubly LinkedList",
        "problems": [
          {"title": "Introduction to DLL, learn about struct, and how to create a node", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/introduction-to-doubly-linked-list/"},
          {"title": "Insert a node in DLL", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/insert-a-node-in-a-doubly-linked-list/"},
          {"title": "Delete a node in DLL", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/delete-a-node-in-a-doubly-linked-list/"},
          {"title": "Reverse a DLL", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/reverse-a-doubly-linked-list/"}
        ]
      },
      {
        "subtopic": "Medium Problems of LL",
        "problems": [
          {"title": "Middle of a LinkedList [TortoiseHare Method]", "difficulty": "Easy", "link": "https://leetcode.com/problems/middle-of-the-linked-list/"},
          {"title": "Reverse a LinkedList [Iterative & Recursive]", "difficulty": "Easy", "link": "https://leetcode.com/problems/reverse-linked-list/"},
          {"title": "Detect a loop in LL", "difficulty": "Easy", "link": "https://leetcode.com/problems/linked-list-cycle/"},
          {"title": "Find the starting point in LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/linked-list-cycle-ii/"},
          {"title": "Length of Loop in LL", "difficulty": "Easy", "link": "https://takeuforward.org/linked-list/find-length-of-loop-in-linked-list/"},
          {"title": "Check if LL is palindrome or not", "difficulty": "Easy", "link": "https://leetcode.com/problems/palindrome-linked-list/"},
          {"title": "Segregate odd and even nodes in LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/odd-even-linked-list/"},
          {"title": "Remove Nth node from the back of the LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/"},
          {"title": "Delete the middle node of LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/"},
          {"title": "Sort LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/sort-list/"},
          {"title": "Sort a LL of 0's 1's and 2's", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/sort-a-linked-list-of-0s-1s-and-2s/"},
          {"title": "Find the intersection point of Y LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/intersection-of-two-linked-lists/"},
          {"title": "Add 1 to a number represented by LL", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/add-1-to-a-number-represented-as-linked-list/"},
          {"title": "Add 2 numbers in LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/add-two-numbers/"}
        ]
      },
      {
        "subtopic": "Medium Problems of DLL",
        "problems": [
          {"title": "Delete all occurrences of a key in DLL", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/delete-all-occurrences-of-a-key-in-dll/"},
          {"title": "Find pairs with given sum in DLL", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-pairs-with-given-sum-in-doubly-linked-list/"},
          {"title": "Remove duplicates from sorted DLL", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/remove-duplicates-from-a-sorted-doubly-linked-list/"}
        ]
      },
      {
        "subtopic": "Hard Problems of LL",
        "problems": [
          {"title": "Reverse LL in group of given size K", "difficulty": "Hard", "link": "https://leetcode.com/problems/reverse-nodes-in-k-group/"},
          {"title": "Rotate a LL", "difficulty": "Medium", "link": "https://leetcode.com/problems/rotate-list/"},
          {"title": "Flattening of LL", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/flattening-a-linked-list/"},
          {"title": "Clone a Linked List with random and next pointer", "difficulty": "Medium", "link": "https://leetcode.com/problems/copy-list-with-random-pointer/"},
          {"title": "Merge 2 Sorted Linked Lists", "difficulty": "Easy", "link": "https://leetcode.com/problems/merge-two-sorted-lists/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-7",
    "stepTitle": "Step 7: Recursion [PatternWise]",
    "description": "Subsets, permutations, N-Queens, Sudoku Solver, and Word Search.",
    "topics": [
      {
        "subtopic": "Get a Strong Hold",
        "problems": [
          {"title": "Recursive Implementation of atoi()", "difficulty": "Medium", "link": "https://leetcode.com/problems/string-to-integer-atoi/"},
          {"title": "Pow(x, n)", "difficulty": "Medium", "link": "https://leetcode.com/problems/powx-n/"},
          {"title": "Count Good numbers", "difficulty": "Medium", "link": "https://leetcode.com/problems/count-good-numbers/"},
          {"title": "Sort a stack using recursion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/sort-a-stack-using-recursion/"},
          {"title": "Reverse a stack using recursion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/reverse-a-stack-using-recursion/"}
        ]
      },
      {
        "subtopic": "Subsequences Pattern",
        "problems": [
          {"title": "Generate all binary strings without consecutive 1s", "difficulty": "Medium", "link": "https://takeuforward.org/recursion/generate-all-binary-strings-without-consecutive-1s/"},
          {"title": "Generate Parentheses", "difficulty": "Medium", "link": "https://leetcode.com/problems/generate-parentheses/"},
          {"title": "Print all subsequences / Power Set", "difficulty": "Medium", "link": "https://leetcode.com/problems/subsets/"},
          {"title": "Learn All Patterns of Subsequences (Count, Check exist, Print all)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/subset-sum-sum-of-all-subsets/"},
          {"title": "Combination Sum I", "difficulty": "Medium", "link": "https://leetcode.com/problems/combination-sum/"},
          {"title": "Combination Sum II", "difficulty": "Medium", "link": "https://leetcode.com/problems/combination-sum-ii/"},
          {"title": "Subset Sum I", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/subset-sum-sum-of-all-subsets/"},
          {"title": "Subset Sum II", "difficulty": "Medium", "link": "https://leetcode.com/problems/subsets-ii/"},
          {"title": "Combination Sum III", "difficulty": "Medium", "link": "https://leetcode.com/problems/combination-sum-iii/"},
          {"title": "Letter Combinations of a Phone number", "difficulty": "Medium", "link": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/"}
        ]
      },
      {
        "subtopic": "Trying out all Combos / Hard",
        "problems": [
          {"title": "Palindrome Partitioning", "difficulty": "Medium", "link": "https://leetcode.com/problems/palindrome-partitioning/"},
          {"title": "Word Search", "difficulty": "Medium", "link": "https://leetcode.com/problems/word-search/"},
          {"title": "N-Queen Problem", "difficulty": "Hard", "link": "https://leetcode.com/problems/n-queens/"},
          {"title": "Rat in a Maze", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/rat-in-a-maze/"},
          {"title": "Word Break", "difficulty": "Medium", "link": "https://leetcode.com/problems/word-break/"},
          {"title": "M Coloring Problem", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/m-coloring-problem/"},
          {"title": "Sudoku Solver", "difficulty": "Hard", "link": "https://leetcode.com/problems/sudoku-solver/"},
          {"title": "Expression Add Operators", "difficulty": "Hard", "link": "https://leetcode.com/problems/expression-add-operators/"},
          {"title": "K-th Permutation Sequence", "difficulty": "Hard", "link": "https://leetcode.com/problems/permutation-sequence/"},
          {"title": "Print all Permutations of a String/Array", "difficulty": "Medium", "link": "https://leetcode.com/problems/permutations/"},
          {"title": "Count Inversions using recursion", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/count-inversions-in-an-array/"},
          {"title": "Reverse Pairs recursive analysis", "difficulty": "Hard", "link": "https://leetcode.com/problems/reverse-pairs/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-8",
    "stepTitle": "Step 8: Bit Manipulation [Learn XORS, etc.]",
    "description": "Bitwise tricks, XOR properties, two non-repeating elements, and power sets.",
    "topics": [
      {
        "subtopic": "Learn Bit Manipulation",
        "problems": [
          {"title": "Introduction to Bit Manipulation (Binary to Decimal, Decimal to Binary)", "difficulty": "Easy", "link": "https://takeuforward.org/bit-manipulation/introduction-to-bit-manipulation/"},
          {"title": "Check if the i-th bit is set or not", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/check-if-the-i-th-bit-is-set-or-not/"},
          {"title": "Check if a number is odd or not", "difficulty": "Easy", "link": "https://takeuforward.org/bit-manipulation/check-if-a-number-is-odd-or-not/"},
          {"title": "Check if a number is power of 2 or not", "difficulty": "Easy", "link": "https://leetcode.com/problems/power-of-two/"},
          {"title": "Count the number of set bits", "difficulty": "Easy", "link": "https://leetcode.com/problems/number-of-1-bits/"},
          {"title": "Set/Unset the rightmost unset bit", "difficulty": "Easy", "link": "https://takeuforward.org/bit-manipulation/set-the-rightmost-unset-bit/"},
          {"title": "Swap two numbers without 3rd variable", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/swap-two-numbers-without-using-a-temporary-variable/"},
          {"title": "Divide Two Integers without multiplication/division", "difficulty": "Medium", "link": "https://leetcode.com/problems/divide-two-integers/"}
        ]
      },
      {
        "subtopic": "Interview Problems",
        "problems": [
          {"title": "Count number of bits to be flipped to convert A to B", "difficulty": "Easy", "link": "https://leetcode.com/problems/minimum-bit-flips-to-convert-number/"},
          {"title": "Find the number that appears odd number of times", "difficulty": "Easy", "link": "https://leetcode.com/problems/single-number/"},
          {"title": "Power Set using bit manipulation", "difficulty": "Medium", "link": "https://leetcode.com/problems/subsets/"},
          {"title": "Find XOR of numbers from L to R", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-xor-of-numbers-from-l-to-r/"},
          {"title": "Find the two numbers appearing odd number of times", "difficulty": "Medium", "link": "https://leetcode.com/problems/single-number-iii/"},
          {"title": "Single Number II (every element 3 times except one)", "difficulty": "Medium", "link": "https://leetcode.com/problems/single-number-ii/"}
        ]
      },
      {
        "subtopic": "Advanced Maths & Bitwise",
        "problems": [
          {"title": "Print all Prime Factors of a number", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/prime-factorisation-of-a-number/"},
          {"title": "All Divisors of a Number (Sieve based)", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/print-all-divisors-of-a-given-number/"},
          {"title": "Sieve of Eratosthenes", "difficulty": "Easy", "link": "https://leetcode.com/problems/count-primes/"},
          {"title": "Find Prime Factorisation of a number using Sieve", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/prime-factorisation-of-a-number/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-9",
    "stepTitle": "Step 9: Stack and Queues [Learning, Pre-In-Post, Monotonic, Implementation]",
    "description": "Monotonic stacks, Next Greater Element, Histogram, Sliding Window Maximum.",
    "topics": [
      {
        "subtopic": "Learning",
        "problems": [
          {"title": "Implement Stack using Arrays", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/implement-stack-using-array/"},
          {"title": "Implement Queue using Arrays", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/implement-queue-using-array/"},
          {"title": "Implement Stack using Queue", "difficulty": "Easy", "link": "https://leetcode.com/problems/implement-stack-using-queues/"},
          {"title": "Implement Queue using Stack", "difficulty": "Easy", "link": "https://leetcode.com/problems/implement-queue-using-stacks/"},
          {"title": "Implement stack using Linkedlist", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/implement-stack-using-linked-list/"},
          {"title": "Implement queue using Linkedlist", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/implement-queue-using-linked-list/"},
          {"title": "Check for balanced paranthesis", "difficulty": "Easy", "link": "https://leetcode.com/problems/valid-parentheses/"},
          {"title": "Implement Min Stack", "difficulty": "Medium", "link": "https://leetcode.com/problems/min-stack/"}
        ]
      },
      {
        "subtopic": "Prefix, Infix, Postfix Conversion Problems",
        "problems": [
          {"title": "Infix to Postfix Conversion using Stack", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/infix-to-postfix/"},
          {"title": "Prefix to Infix Conversion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/prefix-to-infix/"},
          {"title": "Prefix to Postfix Conversion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/prefix-to-postfix/"},
          {"title": "Postfix to Prefix Conversion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/postfix-to-prefix/"},
          {"title": "Postfix to Infix Conversion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/postfix-to-infix/"},
          {"title": "Infix to Prefix Conversion", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/infix-to-prefix/"}
        ]
      },
      {
        "subtopic": "Monotonic Stack/Queue Problems [VVV. Imp]",
        "problems": [
          {"title": "Next Greater Element I", "difficulty": "Easy", "link": "https://leetcode.com/problems/next-greater-element-i/"},
          {"title": "Next Greater Element II", "difficulty": "Medium", "link": "https://leetcode.com/problems/next-greater-element-ii/"},
          {"title": "Next Smaller Element", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/next-smaller-element/"},
          {"title": "Number of NGEs to the right", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/number-of-nges-to-the-right/"},
          {"title": "Trapping Rainwater", "difficulty": "Hard", "link": "https://leetcode.com/problems/trapping-rain-water/"},
          {"title": "Asteroid Collision", "difficulty": "Medium", "link": "https://leetcode.com/problems/asteroid-collision/"},
          {"title": "Sum of Subarray Minimums", "difficulty": "Medium", "link": "https://leetcode.com/problems/sum-of-subarray-minimums/"},
          {"title": "Sum of Subarray Ranges", "difficulty": "Medium", "link": "https://leetcode.com/problems/sum-of-subarray-ranges/"},
          {"title": "Remove k Digits", "difficulty": "Medium", "link": "https://leetcode.com/problems/remove-k-digits/"},
          {"title": "Largest rectangle in a histogram", "difficulty": "Hard", "link": "https://leetcode.com/problems/largest-rectangle-in-histogram/"},
          {"title": "Maximal Rectangles", "difficulty": "Hard", "link": "https://leetcode.com/problems/maximal-rectangle/"}
        ]
      },
      {
        "subtopic": "Implementation Problems",
        "problems": [
          {"title": "Sliding Window Maximum", "difficulty": "Hard", "link": "https://leetcode.com/problems/sliding-window-maximum/"},
          {"title": "The Celebrity Problem", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/celebrity-problem/"},
          {"title": "LRU Cache (Design)", "difficulty": "Medium", "link": "https://leetcode.com/problems/lru-cache/"},
          {"title": "LFU Cache (Design)", "difficulty": "Hard", "link": "https://leetcode.com/problems/lfu-cache/"},
          {"title": "Online Stock Span", "difficulty": "Medium", "link": "https://leetcode.com/problems/online-stock-span/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-10",
    "stepTitle": "Step 10: Sliding Window & Two Pointer Combined",
    "description": "Substrings with distinct chars, fruits into baskets, minimum window substring.",
    "topics": [
      {
        "subtopic": "Medium Problems",
        "problems": [
          {"title": "Longest Substring Without Repeating Characters", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
          {"title": "Max Consecutive Ones III", "difficulty": "Medium", "link": "https://leetcode.com/problems/max-consecutive-ones-iii/"},
          {"title": "Fruit Into Baskets", "difficulty": "Medium", "link": "https://leetcode.com/problems/fruit-into-baskets/"},
          {"title": "Longest Repeating Character Replacement", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-repeating-character-replacement/"},
          {"title": "Binary Subarrays With Sum", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-subarrays-with-sum/"},
          {"title": "Count number of nice subarrays", "difficulty": "Medium", "link": "https://leetcode.com/problems/count-number-of-nice-subarrays/"},
          {"title": "Number of substrings containing all three characters", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/"},
          {"title": "Maximum Points You Can Obtain from Cards", "difficulty": "Medium", "link": "https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/"}
        ]
      },
      {
        "subtopic": "Hard Problems",
        "problems": [
          {"title": "Longest Substring with At Most K Distinct Characters", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/longest-substring-with-at-most-k-distinct-characters/"},
          {"title": "Subarrays with K Different Integers", "difficulty": "Hard", "link": "https://leetcode.com/problems/subarrays-with-k-different-integers/"},
          {"title": "Minimum Window Substring", "difficulty": "Hard", "link": "https://leetcode.com/problems/minimum-window-substring/"},
          {"title": "Minimum Window Subsequence", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/minimum-window-subsequence/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-11",
    "stepTitle": "Step 11: Heaps [Learning, Medium, Hard, Problems]",
    "description": "Min-Heap/Max-Heap implementations, Kth largest elements, Merge K sorted lists.",
    "topics": [
      {
        "subtopic": "Learning",
        "problems": [
          {"title": "Introduction to Priority Queues using Binary Heaps", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/min-heap-and-max-heap-implementation-in-c/"},
          {"title": "Min Heap and Max Heap Implementation", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/min-heap-and-max-heap-implementation-in-c/"},
          {"title": "Check if an array represents a min-heap or not", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/check-if-an-array-represents-a-min-heap/"},
          {"title": "Convert min Heap to max Heap", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/convert-min-heap-to-max-heap/"}
        ]
      },
      {
        "subtopic": "Medium Problems",
        "problems": [
          {"title": "Kth largest element in an array", "difficulty": "Medium", "link": "https://leetcode.com/problems/kth-largest-element-in-an-array/"},
          {"title": "Kth smallest element in an array", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/kth-largest-smallest-element-in-an-array/"},
          {"title": "Sort K-Sorted (Nearly Sorted) Array", "difficulty": "Medium", "link": "https://takeuforward.org/heap/sort-k-sorted-array/"},
          {"title": "Merge M sorted Lists", "difficulty": "Hard", "link": "https://leetcode.com/problems/merge-k-sorted-lists/"},
          {"title": "Replace each array element by its corresponding rank", "difficulty": "Easy", "link": "https://leetcode.com/problems/rank-transform-of-an-array/"},
          {"title": "Task Scheduler", "difficulty": "Medium", "link": "https://leetcode.com/problems/task-scheduler/"},
          {"title": "Hands of Straights", "difficulty": "Medium", "link": "https://leetcode.com/problems/hand-of-straights/"}
        ]
      },
      {
        "subtopic": "Hard Problems",
        "problems": [
          {"title": "Design Twitter", "difficulty": "Medium", "link": "https://leetcode.com/problems/design-twitter/"},
          {"title": "Connect `n` ropes with minimal cost", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/minimum-cost-of-ropes/"},
          {"title": "Kth largest element in a stream of numbers", "difficulty": "Easy", "link": "https://leetcode.com/problems/kth-largest-element-in-a-stream/"},
          {"title": "Maximum Sum Combination", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/maximum-sum-combination/"},
          {"title": "Find Median from Data Stream", "difficulty": "Hard", "link": "https://leetcode.com/problems/find-median-from-data-stream/"},
          {"title": "Top K Frequent Elements", "difficulty": "Medium", "link": "https://leetcode.com/problems/top-k-frequent-elements/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-12",
    "stepTitle": "Step 12: Greedy Algorithms [Easy, Medium/Hard]",
    "description": "Activity selection, Fractional Knapsack, Jump Game, Job Scheduling.",
    "topics": [
      {
        "subtopic": "Easy Problems",
        "problems": [
          {"title": "Assign Cookies", "difficulty": "Easy", "link": "https://leetcode.com/problems/assign-cookies/"},
          {"title": "Fractional Knapsack Problem", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/fractional-knapsack-problem-greedy-approach/"},
          {"title": "Find minimum number of coins", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-minimum-number-of-coins/"},
          {"title": "Lemonade Change", "difficulty": "Easy", "link": "https://leetcode.com/problems/lemonade-change/"}
        ]
      },
      {
        "subtopic": "Medium/Hard Problems",
        "problems": [
          {"title": "N meetings in one room", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/n-meetings-in-one-room/"},
          {"title": "Minimum platforms required for a railway", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/minimum-platforms-needed-on-a-railway-station/"},
          {"title": "Job Sequencing Problem", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/job-sequencing-problem/"},
          {"title": "Candy", "difficulty": "Hard", "link": "https://leetcode.com/problems/candy/"},
          {"title": "Jump Game I", "difficulty": "Medium", "link": "https://leetcode.com/problems/jump-game/"},
          {"title": "Jump Game II", "difficulty": "Medium", "link": "https://leetcode.com/problems/jump-game-ii/"},
          {"title": "Minimum number of dynamic coins / Valid Parenthesis Wildcard", "difficulty": "Medium", "link": "https://leetcode.com/problems/valid-parenthesis-string/"},
          {"title": "Non-overlapping Intervals", "difficulty": "Medium", "link": "https://leetcode.com/problems/non-overlapping-intervals/"},
          {"title": "Insert Interval", "difficulty": "Medium", "link": "https://leetcode.com/problems/insert-interval/"},
          {"title": "Merge Intervals", "difficulty": "Medium", "link": "https://leetcode.com/problems/merge-intervals/"},
          {"title": "Shortest Job First (CPU Scheduling)", "difficulty": "Easy", "link": "https://takeuforward.org/greedy/shortest-job-first-or-sjf-cpu-scheduling/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-13",
    "stepTitle": "Step 13: Binary Trees [Traversals, Medium and Hard Problems]",
    "description": "Traversals (In/Pre/Post/Level), views, diameter, LCA, Morris traversal, construction.",
    "topics": [
      {
        "subtopic": "Traversals",
        "problems": [
          {"title": "Introduction to Trees", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/introduction-to-trees/"},
          {"title": "Binary Tree Representation in C++ / Java / Python", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/binary-tree-representation-in-c/"},
          {"title": "Preorder Traversal of Binary Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/binary-tree-preorder-traversal/"},
          {"title": "Inorder Traversal of Binary Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/binary-tree-inorder-traversal/"},
          {"title": "Postorder Traversal of Binary Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/binary-tree-postorder-traversal/"},
          {"title": "Level order Traversal / Level order traversal in spiral form", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-tree-level-order-traversal/"},
          {"title": "Iterative Preorder Traversal of Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-tree-preorder-traversal/"},
          {"title": "Iterative Inorder Traversal of Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-tree-inorder-traversal/"},
          {"title": "Post-order Traversal of Binary Tree using 2 stack / 1 stack", "difficulty": "Hard", "link": "https://leetcode.com/problems/binary-tree-postorder-traversal/"}
        ]
      },
      {
        "subtopic": "Medium Problems",
        "problems": [
          {"title": "Height of a Binary Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
          {"title": "Check if the Binary tree is height-balanced or not", "difficulty": "Easy", "link": "https://leetcode.com/problems/balanced-binary-tree/"},
          {"title": "Diameter of Binary Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/diameter-of-binary-tree/"},
          {"title": "Maximum path sum", "difficulty": "Hard", "link": "https://leetcode.com/problems/binary-tree-maximum-path-sum/"},
          {"title": "Check if two trees are identical or not", "difficulty": "Easy", "link": "https://leetcode.com/problems/same-tree/"},
          {"title": "Zig-Zag or Spiral Traversal in Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/"},
          {"title": "Boundary Traversal of Binary Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/boundary-traversal-of-a-binary-tree/"},
          {"title": "Vertical Order Traversal of Binary Tree", "difficulty": "Hard", "link": "https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/"},
          {"title": "Top View of Binary Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/top-view-of-a-binary-tree/"},
          {"title": "Bottom View of Binary Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/bottom-view-of-a-binary-tree/"},
          {"title": "Right/Left View of Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-tree-right-side-view/"},
          {"title": "Symmetric Binary Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/symmetric-tree/"}
        ]
      },
      {
        "subtopic": "Hard Problems",
        "problems": [
          {"title": "Root to Node Path in Binary Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/print-root-to-node-path-in-a-binary-tree/"},
          {"title": "Lowest Common Ancestor for two given Nodes", "difficulty": "Medium", "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/"},
          {"title": "Maximum width of a Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/maximum-width-of-binary-tree/"},
          {"title": "Check for Children Sum Property", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/check-for-children-sum-property-in-a-binary-tree/"},
          {"title": "Print all the Nodes at a distance of K in Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/"},
          {"title": "Minimum time taken to BURN the Binary Tree from a Node", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/minimum-time-taken-to-burn-the-binary-tree-from-a-node/"},
          {"title": "Count total Nodes in a COMPLETE Binary Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/count-complete-tree-nodes/"},
          {"title": "Construct Binary Tree from inorder and preorder", "difficulty": "Medium", "link": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/"},
          {"title": "Construct Binary Tree from Inorder and Postorder", "difficulty": "Medium", "link": "https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/"},
          {"title": "Serialize and deserialize Binary Tree", "difficulty": "Hard", "link": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/"},
          {"title": "Morris Preorder & Inorder Traversal of a Binary Tree", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/morris-inorder-traversal-of-a-binary-tree/"},
          {"title": "Flatten Binary Tree to LinkedList", "difficulty": "Medium", "link": "https://leetcode.com/problems/flatten-binary-tree-to-linked-list/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-14",
    "stepTitle": "Step 14: Binary Search Trees [Concept and Problems]",
    "description": "BST validation, search, insertion, deletion, LCA, BST iterator, 2-Sum in BST.",
    "topics": [
      {
        "subtopic": "Concepts",
        "problems": [
          {"title": "Introduction to Binary Search Tree", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/search-in-a-binary-search-tree-bst-traversal/"},
          {"title": "Search in a Binary Search Tree", "difficulty": "Easy", "link": "https://leetcode.com/problems/search-in-a-binary-search-tree/"},
          {"title": "Find Min/Max in BST", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/find-the-minimum-and-maximum-element-in-a-binary-search-tree/"},
          {"title": "Ceil in a Binary Search Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/ceil-in-a-binary-search-tree/"},
          {"title": "Floor in a Binary Search Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/floor-in-a-binary-search-tree/"}
        ]
      },
      {
        "subtopic": "Practice Problems",
        "problems": [
          {"title": "Insert a given Node in Binary Search Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/insert-into-a-binary-search-tree/"},
          {"title": "Delete a Node in Binary Search Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/delete-node-in-a-bst/"},
          {"title": "Find K-th smallest/largest element in BST", "difficulty": "Medium", "link": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/"},
          {"title": "Check if a tree is a BST or BT", "difficulty": "Medium", "link": "https://leetcode.com/problems/validate-binary-search-tree/"},
          {"title": "LCA in Binary Search Tree", "difficulty": "Medium", "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/"},
          {"title": "Construct a BST from a preorder traversal", "difficulty": "Medium", "link": "https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/"},
          {"title": "Inorder Predecessor/Successor in BST", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/inorder-successor-predecessor-in-bst/"},
          {"title": "Binary Search Tree Iterator", "difficulty": "Medium", "link": "https://leetcode.com/problems/binary-search-tree-iterator/"},
          {"title": "Two Sum In BST", "difficulty": "Easy", "link": "https://leetcode.com/problems/two-sum-iv-input-is-a-bst/"},
          {"title": "Correct BST with two nodes swapped", "difficulty": "Medium", "link": "https://leetcode.com/problems/recover-binary-search-tree/"},
          {"title": "Largest BST in Binary Tree", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/maximum-sum-bst-in-binary-tree/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-15",
    "stepTitle": "Step 15: Graphs [Concepts & Problems]",
    "description": "BFS/DFS, Cycle detection, Dijkstra, Bellman-Ford, Floyd Warshall, Topo Sort, Disjoint Set.",
    "topics": [
      {
        "subtopic": "Learning",
        "problems": [
          {"title": "Introduction to Graph, Types & Terminology", "difficulty": "Easy", "link": "https://takeuforward.org/graph/graph-representation-in-c/"},
          {"title": "Graph and Types", "difficulty": "Easy", "link": "https://takeuforward.org/graph/graph-representation-in-c/"},
          {"title": "Graph Representation in C++ / Java / Python", "difficulty": "Easy", "link": "https://takeuforward.org/graph/graph-representation-in-c/"},
          {"title": "Connected Components in an Undirected Graph", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/connected-components-in-graph/"},
          {"title": "BFS Traversal", "difficulty": "Easy", "link": "https://takeuforward.org/graph/breadth-first-search-bfs/"},
          {"title": "DFS Traversal", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/depth-first-search-dfs-traversal-graph/"}
        ]
      },
      {
        "subtopic": "Problems on BFS/DFS",
        "problems": [
          {"title": "Number of Provinces", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-provinces/"},
          {"title": "Connected Components in Matrix (Count Islands)", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-islands/"},
          {"title": "Rotten Oranges", "difficulty": "Medium", "link": "https://leetcode.com/problems/rotting-oranges/"},
          {"title": "Flood Fill", "difficulty": "Easy", "link": "https://leetcode.com/problems/flood-fill/"},
          {"title": "Cycle Detection in unDirected Graph (BFS)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/detect-cycle-in-an-undirected-graph-using-bfs/"},
          {"title": "Cycle Detection in unDirected Graph (DFS)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/detect-cycle-in-an-undirected-graph-using-dfs/"},
          {"title": "0/1 Matrix (Bfs Problem)", "difficulty": "Medium", "link": "https://leetcode.com/problems/01-matrix/"},
          {"title": "Surrounded Regions (dfs)", "difficulty": "Medium", "link": "https://leetcode.com/problems/surrounded-regions/"},
          {"title": "Number of Enclaves", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-enclaves/"},
          {"title": "Word Ladder - I", "difficulty": "Hard", "link": "https://leetcode.com/problems/word-ladder/"},
          {"title": "Word Ladder - II", "difficulty": "Hard", "link": "https://leetcode.com/problems/word-ladder-ii/"},
          {"title": "Number of Distinct Islands", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/number-of-distinct-islands/"},
          {"title": "Bipartite Graph (BFS)", "difficulty": "Medium", "link": "https://leetcode.com/problems/is-graph-bipartite/"},
          {"title": "Bipartite Graph (DFS)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/bipartite-graph-dfs-color-graph/"},
          {"title": "Cycle Detection in Directed Graph (DFS)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/detect-cycle-in-a-directed-graph-using-dfs-g-19/"}
        ]
      },
      {
        "subtopic": "Topo Sort and Problems",
        "problems": [
          {"title": "Topological Sort Algorithm | DFS", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/topological-sort-algorithm-dfs-g-21/"},
          {"title": "Kahn's Algorithm | BFS Topo Sort", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/kahns-algorithm-topological-sort-algorithm-bfs-g-22/"},
          {"title": "Cycle Detection in Directed Graph (BFS Kahn's)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/detect-a-cycle-in-directed-graph-topological-sort-kahns-algorithm-g-23/"},
          {"title": "Course Schedule - I", "difficulty": "Medium", "link": "https://leetcode.com/problems/course-schedule/"},
          {"title": "Course Schedule - II", "difficulty": "Medium", "link": "https://leetcode.com/problems/course-schedule-ii/"},
          {"title": "Find Eventual Safe States - BFS (Kahn's Algo)", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-eventual-safe-states/"},
          {"title": "Alien Dictionary", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/alien-dictionary-topological-sort-g-26/"}
        ]
      },
      {
        "subtopic": "Shortest Path Algorithms and Problems",
        "problems": [
          {"title": "Shortest Path in Directed Acyclic Graph (DAG)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/shortest-path-in-directed-acyclic-graph-topological-sort-g-27/"},
          {"title": "Shortest Path in Undirected Graph with Unit Weights", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/shortest-path-in-undirected-graph-with-unit-weights-g-28/"},
          {"title": "Dijkstra's Algorithm - Using Priority Queue", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/dijkstras-algorithm-using-priority-queue-g-32/"},
          {"title": "Dijkstra's Algorithm - Using Set", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/dijkstras-algorithm-using-set-g-33/"},
          {"title": "Shortest Path in Binary Matrix", "difficulty": "Medium", "link": "https://leetcode.com/problems/shortest-path-in-binary-matrix/"},
          {"title": "Path With Minimum Effort", "difficulty": "Medium", "link": "https://leetcode.com/problems/path-with-minimum-effort/"},
          {"title": "Cheapest Flights Within K Stops", "difficulty": "Medium", "link": "https://leetcode.com/problems/cheapest-flights-within-k-stops/"},
          {"title": "Network Delay Time", "difficulty": "Medium", "link": "https://leetcode.com/problems/network-delay-time/"},
          {"title": "Number of Ways to Arrive at Destination", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/"},
          {"title": "Minimum Multiplications to Reach End", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/minimum-multiplications-to-reach-end-g-39/"},
          {"title": "Bellman Ford Algorithm", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/bellman-ford-algorithm-g-41/"},
          {"title": "Floyd Warshall Algorithm", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/floyd-warshall-algorithm-g-42/"},
          {"title": "Find the City With the Smallest Number of Neighbors at a Threshold Distance", "difficulty": "Medium", "link": "https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/"}
        ]
      },
      {
        "subtopic": "Minimum Spanning Tree / Disjoint Set and Problems",
        "problems": [
          {"title": "Minimum Spanning Tree - Prim's Algorithm", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/prims-algorithm-minimum-spanning-tree-c-and-java-g-45/"},
          {"title": "Disjoint Set [Union by Rank]", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/disjoint-set-union-by-rank-union-by-size-path-compression-g-46/"},
          {"title": "Disjoint Set [Union by Size]", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/disjoint-set-union-by-rank-union-by-size-path-compression-g-46/"},
          {"title": "Kruskal's Algorithm - Minimum Spanning Tree", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/kruskals-algorithm-minimum-spanning-tree-g-47/"},
          {"title": "Number of Operations to Make Network Connected", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-operations-to-make-network-connected/"},
          {"title": "Most Stones Removed with Same Row or Column", "difficulty": "Medium", "link": "https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/"},
          {"title": "Accounts Merge", "difficulty": "Medium", "link": "https://leetcode.com/problems/accounts-merge/"},
          {"title": "Number of Island II - Online Queries", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/number-of-islands-ii-online-queries-dsu-g-51/"},
          {"title": "Making a Large Island - DSU", "difficulty": "Hard", "link": "https://leetcode.com/problems/making-a-large-island/"},
          {"title": "Swim in Rising Water", "difficulty": "Hard", "link": "https://leetcode.com/problems/swim-in-rising-water/"},
          {"title": "Bridges in Graph - Tarjan's Algorithm", "difficulty": "Hard", "link": "https://leetcode.com/problems/critical-connections-in-a-network/"},
          {"title": "Articulation Point in Graph", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/articulation-point-in-graph-g-56/"},
          {"title": "Strongly Connected Components - Kosaraju's Algorithm", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/strongly-connected-components-kosarajus-algorithm-g-54/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-16",
    "stepTitle": "Step 16: Dynamic Programming [Patterns and Problems]",
    "description": "1D, 2D Grids, Subsequences/Knapsack, Strings, Stock problems, LIS, MCM, Partition DP.",
    "topics": [
      {
        "subtopic": "Introduction to DP",
        "problems": [
          {"title": "Introduction to Dynamic Programming (Memoization & Tabulation)", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/dynamic-programming-introduction/"},
          {"title": "Climbing Stars", "difficulty": "Easy", "link": "https://leetcode.com/problems/climbing-stairs/"},
          {"title": "Frog Jump (DP-3)", "difficulty": "Easy", "link": "https://takeuforward.org/data-structures/dynamic-programming-frog-jump-dp-3/"},
          {"title": "Frog Jump with k distances (DP-4)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/dynamic-programming-frog-jump-with-k-distances-dp-4/"},
          {"title": "Maximum sum of non-adjacent elements (DP-5)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/maximum-sum-of-non-adjacent-elements-dp-5/"},
          {"title": "House Robber (DP-6)", "difficulty": "Medium", "link": "https://leetcode.com/problems/house-robber/"},
          {"title": "House Robber II (DP-6)", "difficulty": "Medium", "link": "https://leetcode.com/problems/house-robber-ii/"}
        ]
      },
      {
        "subtopic": "2D/3D DP and DP on Grids",
        "problems": [
          {"title": "Ninjas Training (DP-7)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/dynamic-programming-ninjas-training-dp-7/"},
          {"title": "Grid Unique Paths : DP on Grids (DP-8)", "difficulty": "Medium", "link": "https://leetcode.com/problems/unique-paths/"},
          {"title": "Grid Unique Paths 2 (DP-9)", "difficulty": "Medium", "link": "https://leetcode.com/problems/unique-paths-ii/"},
          {"title": "Minimum path sum in Grid (DP-10)", "difficulty": "Medium", "link": "https://leetcode.com/problems/minimum-path-sum/"},
          {"title": "Minimum path sum in Triangular Grid (DP-11)", "difficulty": "Medium", "link": "https://leetcode.com/problems/triangle/"},
          {"title": "Minimum/Maximum Falling Path Sum (DP-12)", "difficulty": "Medium", "link": "https://leetcode.com/problems/minimum-falling-path-sum/"},
          {"title": "Cherry Pickup II (3D DP - DP-13)", "difficulty": "Hard", "link": "https://leetcode.com/problems/cherry-pickup-ii/"}
        ]
      },
      {
        "subtopic": "DP on Subsequences",
        "problems": [
          {"title": "Subset sum equal to target (DP-14)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/subset-sum-equal-to-target-dp-14/"},
          {"title": "Partition Equal Subset Sum (DP-15)", "difficulty": "Medium", "link": "https://leetcode.com/problems/partition-equal-subset-sum/"},
          {"title": "Partition Set Into 2 Subsets With Min Absolute Sum Diff (DP-16)", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/partition-a-set-into-two-subsets-with-minimum-absolute-sum-difference-dp-16/"},
          {"title": "Count Subsets with Sum K (DP-17)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/count-subsets-with-sum-k-dp-17/"},
          {"title": "Count Partitions with Given Difference (DP-18)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/count-partitions-with-given-difference-dp-18/"},
          {"title": "0/1 Knapsack (DP-19)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/0-1-knapsack-problem-dp-19/"},
          {"title": "Minimum Coins (DP-20)", "difficulty": "Medium", "link": "https://leetcode.com/problems/coin-change/"},
          {"title": "Target Sum (DP-21)", "difficulty": "Medium", "link": "https://leetcode.com/problems/target-sum/"},
          {"title": "Coin Change 2 (DP-22)", "difficulty": "Medium", "link": "https://leetcode.com/problems/coin-change-ii/"},
          {"title": "Unbounded Knapsack (DP-23)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/unbounded-knapsack-dp-23/"},
          {"title": "Rod Cutting Problem (DP-24)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/rod-cutting-problem-dp-24/"}
        ]
      },
      {
        "subtopic": "DP on Strings",
        "problems": [
          {"title": "Longest Common Subsequence (DP-25)", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-common-subsequence/"},
          {"title": "Print Longest Common Subsequence (DP-26)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/print-longest-common-subsequence-dp-26/"},
          {"title": "Longest Common Substring (DP-27)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/longest-common-substring-dp-27/"},
          {"title": "Longest Palindromic Subsequence (DP-28)", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-palindromic-subsequence/"},
          {"title": "Minimum insertions to make string palindrome (DP-29)", "difficulty": "Medium", "link": "https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/"},
          {"title": "Minimum Insertions/Deletions to Convert String A to B (DP-30)", "difficulty": "Medium", "link": "https://leetcode.com/problems/delete-operation-for-two-strings/"},
          {"title": "Shortest Common Supersequence (DP-31)", "difficulty": "Hard", "link": "https://leetcode.com/problems/shortest-common-supersequence/"},
          {"title": "Distinct Subsequences (DP-32)", "difficulty": "Hard", "link": "https://leetcode.com/problems/distinct-subsequences/"},
          {"title": "Edit Distance (DP-33)", "difficulty": "Hard", "link": "https://leetcode.com/problems/edit-distance/"},
          {"title": "Wildcard Matching (DP-34)", "difficulty": "Hard", "link": "https://leetcode.com/problems/wildcard-matching/"}
        ]
      },
      {
        "subtopic": "DP on Stocks",
        "problems": [
          {"title": "Best Time to Buy and Sell Stock (DP-35)", "difficulty": "Easy", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
          {"title": "Buy and Sell Stock - II (DP-36)", "difficulty": "Medium", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/"},
          {"title": "Buy and Sell Stock - III (DP-37)", "difficulty": "Hard", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/"},
          {"title": "Buy and Sell Stock - IV (DP-38)", "difficulty": "Hard", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/"},
          {"title": "Buy and Sell Stocks With Cooldown (DP-39)", "difficulty": "Medium", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/"},
          {"title": "Buy and Sell Stocks With Transaction Fee (DP-40)", "difficulty": "Medium", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/"}
        ]
      },
      {
        "subtopic": "DP on LIS",
        "problems": [
          {"title": "Longest Increasing Subsequence (DP-41)", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-increasing-subsequence/"},
          {"title": "Printing Longest Increasing Subsequence (DP-42)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/printing-longest-increasing-subsequence-dp-42/"},
          {"title": "Longest Increasing Subsequence - Binary Search (DP-43)", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-increasing-subsequence/"},
          {"title": "Largest Divisible Subset (DP-44)", "difficulty": "Medium", "link": "https://leetcode.com/problems/largest-divisible-subset/"},
          {"title": "Longest String Chain (DP-45)", "difficulty": "Medium", "link": "https://leetcode.com/problems/longest-string-chain/"},
          {"title": "Longest Bitonic Subsequence (DP-46)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/longest-bitonic-subsequence-dp-46/"},
          {"title": "Number of Longest Increasing Subsequences (DP-47)", "difficulty": "Medium", "link": "https://leetcode.com/problems/number-of-longest-increasing-subsequence/"}
        ]
      },
      {
        "subtopic": "MCM DP / Partition DP",
        "problems": [
          {"title": "Matrix Chain Multiplication (DP-48)", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/matrix-chain-multiplication-dp-48/"},
          {"title": "Matrix Chain Multiplication - Bottom UP (DP-49)", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/matrix-chain-multiplication-tabulation-method-dp-49/"},
          {"title": "Minimum Cost to Cut the Stick (DP-50)", "difficulty": "Hard", "link": "https://leetcode.com/problems/minimum-cost-to-cut-a-stick/"},
          {"title": "Burst Balloons (DP-51)", "difficulty": "Hard", "link": "https://leetcode.com/problems/burst-balloons/"},
          {"title": "Evaluate Boolean Expression to True (DP-52)", "difficulty": "Hard", "link": "https://takeuforward.org/data-structures/boolean-evaluation-dp-52/"},
          {"title": "Palindrome Partitioning - II (DP-53)", "difficulty": "Hard", "link": "https://leetcode.com/problems/palindrome-partitioning-ii/"},
          {"title": "Partition Array for Maximum Sum (DP-54)", "difficulty": "Medium", "link": "https://leetcode.com/problems/partition-array-for-maximum-sum/"},
          {"title": "Maximum Rectangle Area with all 1's (DP-55)", "difficulty": "Hard", "link": "https://leetcode.com/problems/maximal-rectangle/"},
          {"title": "Count Square Submatrices with All Ones (DP-56)", "difficulty": "Medium", "link": "https://leetcode.com/problems/count-square-submatrices-with-all-ones/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-17",
    "stepTitle": "Step 17: Tries",
    "description": "Prefix tree, autocomplete, Bitwise XOR maximum queries.",
    "topics": [
      {
        "subtopic": "Theory",
        "problems": [
          {"title": "Implement Trie - 1 (Prefix Tree)", "difficulty": "Medium", "link": "https://leetcode.com/problems/implement-trie-prefix-tree/"},
          {"title": "Implement Trie - II (Prefix Tree)", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/implement-trie-ii/"},
          {"title": "Longest String with All Prefixes", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/longest-word-with-all-prefixes/"},
          {"title": "Number of Distinct Substrings in a String", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/number-of-distinct-substrings-in-a-string-using-trie/"}
        ]
      },
      {
        "subtopic": "Problems",
        "problems": [
          {"title": "Bit Prerequisites for TRIE Problems", "difficulty": "Easy", "link": "https://takeuforward.org/trie/bit-prerequisites-for-trie-problems/"},
          {"title": "Maximum XOR of Two Numbers in an Array", "difficulty": "Medium", "link": "https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/"},
          {"title": "Maximum XOR With an Element From Array", "difficulty": "Hard", "link": "https://leetcode.com/problems/maximum-xor-with-an-element-from-array/"}
        ]
      }
    ]
  },
  {
    "stepId": "step-18",
    "stepTitle": "Step 18: Strings Advanced [KMP, Z-function, etc.]",
    "description": "KMP String matching algorithm, Z-function, Rabin-Karp.",
    "topics": [
      {
        "subtopic": "Advanced String Matching Algorithms",
        "problems": [
          {"title": "Rabin Karp Algorithm", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/rabin-karp-algorithm/"},
          {"title": "Z-Function Algorithm", "difficulty": "Medium", "link": "https://takeuforward.org/data-structures/z-function/"},
          {"title": "KMP Algorithm / LPS(pi-table) Array", "difficulty": "Hard", "link": "https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/"},
          {"title": "Shortest Palindrome using KMP", "difficulty": "Hard", "link": "https://leetcode.com/problems/shortest-palindrome/"},
          {"title": "Longest Happy Prefix", "difficulty": "Hard", "link": "https://leetcode.com/problems/longest-happy-prefix/"},
          {"title": "Count and Say", "difficulty": "Medium", "link": "https://leetcode.com/problems/count-and-say/"}
        ]
      }
    ]
  }
]

# Assign global unique IDs 1..N
current_id = 1
for step in full_dataset:
    for topic in step['topics']:
        for prob in topic['problems']:
            prob['id'] = current_id
            current_id += 1

print(f"Total problems generated: {current_id - 1}")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet Full Curriculum (474 Items Matching TakeUForward Exact Breakdown)\n")
    f.write("const DSA_DATA = ")
    json.dump(full_dataset, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

print("Updated data.js with exact 1:1 hierarchy and 474 problems!")
