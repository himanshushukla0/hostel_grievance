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

# Real-world Market & Quant applications mapped 1:1 to every single DSA step
market_extensions = {
  "step-1": {
    "subtopic": "🚀 Quant & Market Application: Float Rounding & Fixed-Point Math",
    "problems": [
      {
        "title": "Quant Concept: Fixed-Point Math in Stock Exchanges (Why Floats are Forbidden in Trading Engines)",
        "difficulty": "Easy",
        "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
        "article": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
        "youtube": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
        "leetcode": None
      }
    ]
  },
  "step-2": {
    "subtopic": "🚀 Quant & Market Application: Price-Time Priority Matching",
    "problems": [
      {
        "title": "Quant Concept: How Exchange Matching Engines Sort Orders by Price-Time Priority",
        "difficulty": "Easy",
        "link": "https://www.quantconnect.com/learning",
        "article": "https://en.wikipedia.org/wiki/Order_(exchange)#Price-time_priority",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": None
      }
    ]
  },
  "step-3": {
    "subtopic": "🚀 Quant & Market Application: Candlestick Streams & Tick Buffers",
    "problems": [
      {
        "title": "Quant Concept: Processing Real-Time OHLC (Open-High-Low-Close) Candlestick Buffers in C++",
        "difficulty": "Medium",
        "link": "https://www.quantconnect.com/learning",
        "article": "https://en.wikipedia.org/wiki/Candlestick_chart",
        "youtube": "https://www.youtube.com/watch?v=UXDSeD9mN-k",
        "leetcode": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"
      }
    ]
  },
  "step-4": {
    "subtopic": "🚀 Quant & Market Application: Finding Implied Volatility with Binary Search",
    "problems": [
      {
        "title": "Quant Concept: Binary Search on Search Space to Calculate Implied Volatility (IV) from Black-Scholes",
        "difficulty": "Medium",
        "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
        "article": "https://en.wikipedia.org/wiki/Implied_volatility",
        "youtube": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
        "leetcode": "https://leetcode.com/problems/sqrtx/"
      }
    ]
  },
  "step-5": {
    "subtopic": "🚀 Quant & Market Application: High-Speed FIX Message Parsing",
    "problems": [
      {
        "title": "Quant Concept: Zero-Allocation Tag-Value String Parsing for FIX Protocol (Financial Information eXchange)",
        "difficulty": "Medium",
        "link": "https://www.fixtrading.org/what-is-fix/",
        "article": "https://www.fixtrading.org/what-is-fix/",
        "youtube": "https://www.youtube.com/watch?v=2Tz8XUu4R-4",
        "leetcode": None
      }
    ]
  },
  "step-6": {
    "subtopic": "🚀 Quant & Market Application: O(1) Limit Order Queue with Doubly Linked Lists",
    "problems": [
      {
        "title": "Quant Concept: Why Limit Order Books use Doubly Linked Lists for O(1) Order Cancellation",
        "difficulty": "Medium",
        "link": "https://github.com/topics/orderbook",
        "article": "https://en.wikipedia.org/wiki/Order_book",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": "https://leetcode.com/problems/lru-cache/"
      }
    ]
  },
  "step-7": {
    "subtopic": "🚀 Quant & Market Application: Binomial Options Pricing Trees",
    "problems": [
      {
        "title": "Quant Concept: Recursive Cox-Ross-Rubinstein (CRR) Tree for American Option Pricing",
        "difficulty": "Hard",
        "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
        "article": "https://en.wikipedia.org/wiki/Binomial_options_pricing_model",
        "youtube": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
        "leetcode": None
      }
    ]
  },
  "step-8": {
    "subtopic": "🚀 Quant & Market Application: 64-Bit Compact Order Ticket Packing",
    "problems": [
      {
        "title": "Quant Concept: Packing Order Type, Side, Quantity & Flags into Single 64-Bit Word with Bitmasks",
        "difficulty": "Medium",
        "link": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/resources/lecture-3-bit-hacks/",
        "article": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
        "youtube": "https://www.youtube.com/watch?v=o7b_5sWbTz4",
        "leetcode": None
      }
    ]
  },
  "step-9": {
    "subtopic": "🚀 Quant & Market Application: SPSC Lock-Free Ring Buffers & Stock Span",
    "problems": [
      {
        "title": "Quant Concept: Lock-Free Single-Producer Single-Consumer Queue & Real-Time Stock Span Analysis",
        "difficulty": "Hard",
        "link": "https://en.cppreference.com/w/cpp/atomic/atomic",
        "article": "https://www.boost.org/doc/libs/release/doc/html/lockfree.html",
        "youtube": "https://www.youtube.com/watch?v=Kowv-Gj_K_A",
        "leetcode": "https://leetcode.com/problems/online-stock-span/"
      }
    ]
  },
  "step-10": {
    "subtopic": "🚀 Quant & Market Application: Real-Time Rolling VWAP & Bollinger Bands",
    "problems": [
      {
        "title": "Quant Concept: Sliding Window Algorithms for Real-Time VWAP and Bollinger Band Volatility",
        "difficulty": "Medium",
        "link": "https://www.quantconnect.com/learning",
        "article": "https://en.wikipedia.org/wiki/Bollinger_Bands",
        "youtube": "https://www.youtube.com/watch?v=sI9U8n0uGqI",
        "leetcode": None
      }
    ]
  },
  "step-11": {
    "subtopic": "🚀 Quant & Market Application: Multi-Exchange Chronological Tick Merger",
    "problems": [
      {
        "title": "Quant Concept: Merging Asynchronous Tick Feeds from NSE, BSE & MCX using Min-Heap",
        "difficulty": "Medium",
        "link": "https://www.quantconnect.com/learning",
        "article": "https://en.wikipedia.org/wiki/Priority_queue",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": "https://leetcode.com/problems/merge-k-sorted-lists/"
      }
    ]
  },
  "step-12": {
    "subtopic": "🚀 Quant & Market Application: Smart Order Routing (SOR) across Venues",
    "problems": [
      {
        "title": "Quant Concept: Greedy Algorithms in Smart Order Routing (SOR) for Minimum Transaction Costs",
        "difficulty": "Medium",
        "link": "https://en.wikipedia.org/wiki/Smart_order_routing",
        "article": "https://en.wikipedia.org/wiki/Smart_order_routing",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": None
      }
    ]
  },
  "step-13": {
    "subtopic": "🚀 Quant & Market Application: Order Book Depth Trees",
    "problems": [
      {
        "title": "Quant Concept: Binary Tree Traversals for Calculating Cumulative Depth-of-Market (DOM)",
        "difficulty": "Medium",
        "link": "https://en.wikipedia.org/wiki/Order_book",
        "article": "https://en.wikipedia.org/wiki/Order_book",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": None
      }
    ]
  },
  "step-14": {
    "subtopic": "🚀 Quant & Market Application: Self-Balancing Price Ladders",
    "problems": [
      {
        "title": "Quant Concept: Red-Black Trees & AVL Trees for Dynamic Limit Order Price Level Discovery",
        "difficulty": "Medium",
        "link": "https://github.com/topics/orderbook",
        "article": "https://en.wikipedia.org/wiki/Red%E2%80%93black_tree",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": None
      }
    ]
  },
  "step-15": {
    "subtopic": "🚀 Quant & Market Application: Triangular Currency Arbitrage in Forex/Crypto",
    "problems": [
      {
        "title": "Quant Concept: Detecting Triangular Currency Arbitrage Cycles with Negative-Cycle Bellman-Ford",
        "difficulty": "Hard",
        "link": "https://en.wikipedia.org/wiki/Triangular_arbitrage",
        "article": "https://en.wikipedia.org/wiki/Triangular_arbitrage",
        "youtube": "https://www.youtube.com/watch?v=0hY7_o6sEps",
        "leetcode": None
      }
    ]
  },
  "step-16": {
    "subtopic": "🚀 Quant & Market Application: Almgren-Chriss Optimal Execution",
    "problems": [
      {
        "title": "Quant Concept: Dynamic Programming in the Almgren-Chriss Model for Minimizing Market Impact",
        "difficulty": "Hard",
        "link": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
        "article": "https://en.wikipedia.org/wiki/Optimal_execution",
        "youtube": "https://www.youtube.com/watch?v=uzkc-qNVoOk",
        "leetcode": None
      }
    ]
  },
  "step-17": {
    "subtopic": "🚀 Quant & Market Application: Ultra-Fast Security Ticker Routing",
    "problems": [
      {
        "title": "Quant Concept: Trie & Radix Trees for Nanosecond Symbol Routing & ISIN Identifier Lookup",
        "difficulty": "Medium",
        "link": "https://en.wikipedia.org/wiki/Trie",
        "article": "https://en.wikipedia.org/wiki/Trie",
        "youtube": "https://www.youtube.com/watch?v=b1e4t2k2KJY",
        "leetcode": "https://leetcode.com/problems/implement-trie-prefix-tree/"
      }
    ]
  },
  "step-18": {
    "subtopic": "🚀 Quant & Market Application: High-Speed News Feed Sentiment Matching",
    "problems": [
      {
        "title": "Quant Concept: KMP & Aho-Corasick Multi-Pattern Matching for Automated Breaking News Trading Bots",
        "difficulty": "Hard",
        "link": "https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm",
        "article": "https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm",
        "youtube": "https://www.youtube.com/watch?v=0hY7_o6sEps",
        "leetcode": None
      }
    ]
  }
}

next_id = max_id + 1
added_count = 0

for step in data:
    sid = step['stepId']
    if sid in market_extensions:
        ext = market_extensions[sid]
        # Check if already added
        existing_subtopics = [t['subtopic'] for t in step['topics']]
        if ext['subtopic'] not in existing_subtopics:
            new_problems = []
            for p in ext['problems']:
                p_copy = dict(p)
                p_copy['id'] = next_id
                next_id += 1
                new_problems.append(p_copy)
                added_count += 1
            
            step['topics'].append({
                "subtopic": ext['subtopic'],
                "problems": new_problems
            })

print(f"Appended {added_count} Market & Quant application topics directly into Steps 1 to 18!")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet + Unified Step-by-Step Market & Quant Foundations\n")
    f.write("const DSA_DATA = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

total = sum(len(t['problems']) for s in data for t in s['topics'])
print(f"New Grand Total Problems in Vault: {total}")
