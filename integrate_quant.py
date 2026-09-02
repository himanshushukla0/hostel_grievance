import json

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Extract existing DSA_DATA array
json_str = code.split('const DSA_DATA = ')[1].rsplit(';', 1)[0].rsplit(';\n', 1)[0]
data = json.loads(json_str)

# Find max ID
max_id = 0
for s in data:
    for t in s['topics']:
        for p in t['problems']:
            if p.get('id', 0) > max_id:
                max_id = p.get('id', 0)

print("Current max ID:", max_id, "Current steps:", len(data))

# Define Quant & HFT Integrated Steps
quant_steps = [
  {
    "stepId": "step-19",
    "stepTitle": "Step 19: Quant & HFT Engineering [Low-Latency C++, Memory & Lock-Free]",
    "description": "Hardware-level optimizations, CPU cache lines, Limit Order Book (LOB), and lock-free concurrency.",
    "topics": [
      {
        "subtopic": "Market Microstructure & Order Book Architecture",
        "problems": [
          {
            "id": max_id + 1,
            "title": "Design High-Frequency Limit Order Book (LOB) in C++ (O(1) Cancel, Price-Time Priority)",
            "difficulty": "Hard",
            "link": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "article": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "youtube": "https://www.youtube.com/watch?v=o7b_5sWbTz4",
            "leetcode": "https://leetcode.com/problems/design-a-leaderboard/"
          },
          {
            "id": max_id + 2,
            "title": "L2 / L3 Market Data Feed & Order Book Matching Engine",
            "difficulty": "Hard",
            "link": "https://github.com/topics/orderbook",
            "article": "https://www.quantconnect.com/learning",
            "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
            "leetcode": None
          },
          {
            "id": max_id + 3,
            "title": "Fast Packet Parser for FIX Protocol / Binary Market Ticks",
            "difficulty": "Medium",
            "link": "https://www.fixtrading.org/what-is-fix/",
            "article": "https://www.fixtrading.org/what-is-fix/",
            "youtube": "https://www.youtube.com/watch?v=2Tz8XUu4R-4",
            "leetcode": None
          }
        ]
      },
      {
        "subtopic": "Low-Latency C++ & Hardware-Aware Systems (MIT 6.172 Core)",
        "problems": [
          {
            "id": max_id + 4,
            "title": "Cache-Conscious Matrix & Tick Traversal (L1/L2 Cache Lines & Avoiding Cache Misses)",
            "difficulty": "Medium",
            "link": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/resources/lecture-3-bit-hacks/",
            "article": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "youtube": "https://www.youtube.com/watch?v=o7b_5sWbTz4",
            "leetcode": None
          },
          {
            "id": max_id + 5,
            "title": "Bit Manipulation in HFT: Fast Bit Hacks & Compact Order Flag Packing",
            "difficulty": "Medium",
            "link": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/resources/lecture-3-bit-hacks/",
            "article": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "youtube": "https://www.youtube.com/watch?v=o7b_5sWbTz4",
            "leetcode": "https://leetcode.com/problems/number-of-1-bits/"
          },
          {
            "id": max_id + 6,
            "title": "Memory Alignment, False Sharing Prevention & `alignas(64)` in Multithreaded C++",
            "difficulty": "Hard",
            "link": "https://en.cppreference.com/w/cpp/language/alignas",
            "article": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "youtube": "https://www.youtube.com/watch?v=WDIkqP4JbkE",
            "leetcode": None
          },
          {
            "id": max_id + 7,
            "title": "Zero-Copy Memory Design & Move Semantics (`std::move`, Rvalue References)",
            "difficulty": "Medium",
            "link": "https://en.cppreference.com/w/cpp/utility/move",
            "article": "https://isocpp.org/wiki/faq/cpp11-language#rvalue-refs",
            "youtube": "https://www.youtube.com/watch?v=IOkgRHmWtE0",
            "leetcode": None
          }
        ]
      },
      {
        "subtopic": "Lock-Free Concurrency & Real-Time Queues",
        "problems": [
          {
            "id": max_id + 8,
            "title": "Single-Producer Single-Consumer (SPSC) Lock-Free Ring Buffer in C++ (`std::atomic`)",
            "difficulty": "Hard",
            "link": "https://en.cppreference.com/w/cpp/atomic/atomic",
            "article": "https://www.boost.org/doc/libs/release/doc/html/lockfree.html",
            "youtube": "https://www.youtube.com/watch?v=Kowv-Gj_K_A",
            "leetcode": "https://leetcode.com/problems/design-circular-queue/"
          },
          {
            "id": max_id + 9,
            "title": "C++ Atomic Memory Ordering: `std::memory_order_relaxed`, `acquire`, and `release`",
            "difficulty": "Hard",
            "link": "https://en.cppreference.com/w/cpp/atomic/memory_order",
            "article": "https://en.cppreference.com/w/cpp/atomic/memory_order",
            "youtube": "https://www.youtube.com/watch?v=ZQFzMfHIxng",
            "leetcode": None
          },
          {
            "id": max_id + 10,
            "title": "Linux CPU Pinning (`pthread_setaffinity_np`) & Thread Core Isolation for Ultra-Low Latency",
            "difficulty": "Medium",
            "link": "https://man7.org/linux/man-pages/man3/pthread_setaffinity_np.3.html",
            "article": "https://man7.org/linux/man-pages/man3/pthread_setaffinity_np.3.html",
            "youtube": "https://www.youtube.com/watch?v=NH1Tta7purM",
            "leetcode": None
          }
        ]
      }
    ]
  },
  {
    "stepId": "step-20",
    "stepTitle": "Step 20: Quant Research, Probability & Market Algorithms [Jane Street / Optiver]",
    "description": "Probability models, statistical arbitrage, market making, and expected value brainteasers.",
    "topics": [
      {
        "subtopic": "Probability & Expected Value Brainteasers (Jane Street / Citadel Core)",
        "problems": [
          {
            "id": max_id + 11,
            "title": "The Fair Dice Re-roll Game & Optimal Stopping Rule (Expected Value Optimization)",
            "difficulty": "Easy",
            "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "article": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "youtube": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
            "leetcode": None
          },
          {
            "id": max_id + 12,
            "title": "Kelly Criterion & Optimal Bet Sizing for Positive Expectancy Trading",
            "difficulty": "Medium",
            "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "article": "https://en.wikipedia.org/wiki/Kelly_criterion",
            "youtube": "https://www.youtube.com/watch?v=H7_4y488W3k",
            "leetcode": None
          },
          {
            "id": max_id + 13,
            "title": "Conditional Probability & Bayesian Updating (The 3 Cards / Monty Hall Problem)",
            "difficulty": "Easy",
            "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "article": "https://en.wikipedia.org/wiki/Monty_Hall_problem",
            "youtube": "https://www.youtube.com/watch?v=4Lb-6rxZxx0",
            "leetcode": None
          },
          {
            "id": max_id + 14,
            "title": "Random Walks & Gambler's Ruin Problem (Markov Chains in Stock Price Models)",
            "difficulty": "Medium",
            "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "article": "https://en.wikipedia.org/wiki/Gambler%27s_ruin",
            "youtube": "https://www.youtube.com/watch?v=63HvvfWjS8c",
            "leetcode": None
          }
        ]
      },
      {
        "subtopic": "Statistical Arbitrage & Market Algorithms",
        "problems": [
          {
            "id": max_id + 15,
            "title": "Pairs Trading & Cointegration Analysis (Mean Reverting Spread Tracker in C++/Python)",
            "difficulty": "Medium",
            "link": "https://www.quantconnect.com/learning",
            "article": "https://www.quantconnect.com/learning",
            "youtube": "https://www.youtube.com/watch?v=0hY7_o6sEps",
            "leetcode": None
          },
          {
            "id": max_id + 16,
            "title": "VWAP (Volume-Weighted Average Price) & TWAP Optimal Execution Algorithm",
            "difficulty": "Medium",
            "link": "https://www.quantconnect.com/learning",
            "article": "https://en.wikipedia.org/wiki/Volume-weighted_average_price",
            "youtube": "https://www.youtube.com/watch?v=sI9U8n0uGqI",
            "leetcode": None
          },
          {
            "id": max_id + 17,
            "title": "Simple & Exponential Moving Average (SMA/EMA) Streaming Crossover Engine",
            "difficulty": "Easy",
            "link": "https://www.quantconnect.com/learning",
            "article": "https://www.quantconnect.com/learning",
            "youtube": "https://www.youtube.com/watch?v=V8kHqQ9a6oM",
            "leetcode": "https://leetcode.com/problems/moving-average-from-data-stream/"
          }
        ]
      },
      {
        "subtopic": "World-Class Academic Courses & Open Labs",
        "problems": [
          {
            "id": max_id + 18,
            "title": "MIT 6.172: Performance Engineering of Software Systems (Full Course & Video Lectures)",
            "difficulty": "Hard",
            "link": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "article": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
            "youtube": "https://www.youtube.com/watch?v=o7b_5sWbTz4",
            "leetcode": None
          },
          {
            "id": max_id + 19,
            "title": "Stanford CS149: Parallel Computing & Multiprocessor Architecture",
            "difficulty": "Hard",
            "link": "http://kayvonf.com/cs149/",
            "article": "http://kayvonf.com/cs149/",
            "youtube": "https://www.youtube.com/watch?v=3Z4n03q2yqA",
            "leetcode": None
          },
          {
            "id": max_id + 20,
            "title": "MIT 18.S096: Topics in Mathematics with Applications in Finance",
            "difficulty": "Medium",
            "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "article": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
            "youtube": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
            "leetcode": None
          }
        ]
      }
    ]
  }
]

# Append if not already present
has_step_19 = any(s['stepId'] == 'step-19' for s in data)
if not has_step_19:
    data.extend(quant_steps)
    print(f"Added {len(quant_steps)} new Quant & HFT steps!")

# Save to data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet + Integrated Quant & HFT Low-Latency Curriculum\n")
    f.write("const DSA_DATA = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

# Count total
total = sum(len(t['problems']) for s in data for t in s['topics'])
print(f"Total problems in unified vault: {total}")
