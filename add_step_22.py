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

print(f"Current max ID: {max_id}, Current Total Steps: {len(data)}")

step_22 = {
    "stepId": "step-22",
    "stepTitle": "Step 22: Core CS Subjects, SQL Top 50 & LLD Machine Coding [Interview Mastery]",
    "description": "Essential interview syllabus for 2nd/3rd year internships: Operating Systems, DBMS & SQL Top 50, OOPs in C++, Computer Networks & Low-Level Design.",
    "topics": [
        {
            "subtopic": "Top 50 Interview SQL Queries (LeetCode SQL 50 Benchmark)",
            "problems": [
                {
                    "id": max_id + 1,
                    "title": "SQL: Combine Two Tables (Left Outer Join on Person & Address)",
                    "difficulty": "Easy",
                    "link": "https://leetcode.com/problems/combine-two-tables/",
                    "leetcode": "https://leetcode.com/problems/combine-two-tables/",
                    "article": "https://leetcode.com/problems/combine-two-tables/solution/",
                    "youtube": "https://www.youtube.com/watch?v=k-a8d6e9qH0"
                },
                {
                    "id": max_id + 2,
                    "title": "SQL: Second Highest Salary (Subquery vs DENSE_RANK() vs LIMIT/OFFSET)",
                    "difficulty": "Medium",
                    "link": "https://leetcode.com/problems/second-highest-salary/",
                    "leetcode": "https://leetcode.com/problems/second-highest-salary/",
                    "article": "https://leetcode.com/problems/second-highest-salary/solution/",
                    "youtube": "https://www.youtube.com/watch?v=F0J3e9V4z0Q"
                },
                {
                    "id": max_id + 3,
                    "title": "SQL: Department Top Three Salaries (Window Function DENSE_RANK() OVER PARTITION BY)",
                    "difficulty": "Hard",
                    "link": "https://leetcode.com/problems/department-top-three-salaries/",
                    "leetcode": "https://leetcode.com/problems/department-top-three-salaries/",
                    "article": "https://leetcode.com/problems/department-top-three-salaries/solution/",
                    "youtube": "https://www.youtube.com/watch?v=XzWz2x4M-e4"
                },
                {
                    "id": max_id + 4,
                    "title": "SQL: Consecutive Numbers (Window Functions LEAD() & LAG() vs Multi-Table Self Join)",
                    "difficulty": "Medium",
                    "link": "https://leetcode.com/problems/consecutive-numbers/",
                    "leetcode": "https://leetcode.com/problems/consecutive-numbers/",
                    "article": "https://leetcode.com/problems/consecutive-numbers/solution/",
                    "youtube": "https://www.youtube.com/watch?v=wX-y8T0P-hA"
                },
                {
                    "id": max_id + 5,
                    "title": "SQL: Employees Earning More Than Their Managers (Self Join & Subqueries)",
                    "difficulty": "Easy",
                    "link": "https://leetcode.com/problems/employees-earning-more-than-their-managers/",
                    "leetcode": "https://leetcode.com/problems/employees-earning-more-than-their-managers/",
                    "article": "https://leetcode.com/problems/employees-earning-more-than-their-managers/solution/",
                    "youtube": "https://www.youtube.com/watch?v=eYkZ-xZ-5e8"
                },
                {
                    "id": max_id + 6,
                    "title": "SQL: Duplicate Emails (GROUP BY ... HAVING COUNT(*) > 1)",
                    "difficulty": "Easy",
                    "link": "https://leetcode.com/problems/duplicate-emails/",
                    "leetcode": "https://leetcode.com/problems/duplicate-emails/",
                    "article": "https://leetcode.com/problems/duplicate-emails/solution/",
                    "youtube": "https://www.youtube.com/watch?v=hG9w4y-x-8g"
                },
                {
                    "id": max_id + 7,
                    "title": "SQL: Delete Duplicate Emails in-place (Self Join with DELETE statement)",
                    "difficulty": "Easy",
                    "link": "https://leetcode.com/problems/delete-duplicate-emails/",
                    "leetcode": "https://leetcode.com/problems/delete-duplicate-emails/",
                    "article": "https://leetcode.com/problems/delete-duplicate-emails/solution/",
                    "youtube": "https://www.youtube.com/watch?v=Kz6m2o9w0L8"
                },
                {
                    "id": max_id + 8,
                    "title": "SQL: Rising Temperature (DATEDIFF() & Cross Join for Date Comparisons)",
                    "difficulty": "Easy",
                    "link": "https://leetcode.com/problems/rising-temperature/",
                    "leetcode": "https://leetcode.com/problems/rising-temperature/",
                    "article": "https://leetcode.com/problems/rising-temperature/solution/",
                    "youtube": "https://www.youtube.com/watch?v=yW9k2mP-Q8w"
                },
                {
                    "id": max_id + 9,
                    "title": "SQL: Trips and Users (Conditional Aggregation with ROUND, CASE WHEN & Filters)",
                    "difficulty": "Hard",
                    "link": "https://leetcode.com/problems/trips-and-users/",
                    "leetcode": "https://leetcode.com/problems/trips-and-users/",
                    "article": "https://leetcode.com/problems/trips-and-users/solution/",
                    "youtube": "https://www.youtube.com/watch?v=0kF4t9wQ8_g"
                },
                {
                    "id": max_id + 10,
                    "title": "SQL: Last Person to Fit in the Bus (Running Cumulative SUM() OVER (ORDER BY...))",
                    "difficulty": "Medium",
                    "link": "https://leetcode.com/problems/last-person-to-fit-in-the-bus/",
                    "leetcode": "https://leetcode.com/problems/last-person-to-fit-in-the-bus/",
                    "article": "https://leetcode.com/problems/last-person-to-fit-in-the-bus/solution/",
                    "youtube": "https://www.youtube.com/watch?v=L-K8w0xY-Q4"
                },
                {
                    "id": max_id + 11,
                    "title": "SQL: Restaurant Growth (7-Day Rolling Moving Average in Pure SQL)",
                    "difficulty": "Medium",
                    "link": "https://leetcode.com/problems/restaurant-growth/",
                    "leetcode": "https://leetcode.com/problems/restaurant-growth/",
                    "article": "https://leetcode.com/problems/restaurant-growth/solution/",
                    "youtube": "https://www.youtube.com/watch?v=eYkZ-xZ-5e8"
                }
            ]
        },
        {
            "subtopic": "Object-Oriented Programming (OOPs) in C++",
            "problems": [
                {
                    "id": max_id + 12,
                    "title": "OOPs: The 4 Pillars (Polymorphism, Inheritance, Encapsulation, Abstraction in C++)",
                    "difficulty": "Easy",
                    "link": "https://www.geeksforgeeks.org/object-oriented-programming-in-cpp/",
                    "article": "https://takeuforward.org/oops/oops-concepts-in-cpp/",
                    "youtube": "https://www.youtube.com/watch?v=wN0x9eZLlf4",
                    "abdul_bari": "https://www.youtube.com/watch?v=9TlHvipP5yA"
                },
                {
                    "id": max_id + 13,
                    "title": "OOPs: Virtual Functions, VTables & Dynamic Runtime Dispatch Mechanism",
                    "difficulty": "Medium",
                    "link": "https://en.cppreference.com/w/cpp/language/virtual",
                    "article": "https://takeuforward.org/oops/virtual-functions-and-runtime-polymorphism/",
                    "youtube": "https://www.youtube.com/watch?v=Z_vJEb9GoZQ"
                },
                {
                    "id": max_id + 14,
                    "title": "OOPs: Shallow Copy vs Deep Copy, Copy Constructor & Rule of 5 in Modern C++",
                    "difficulty": "Medium",
                    "link": "https://en.cppreference.com/w/cpp/language/rule_of_three",
                    "article": "https://isocpp.org/wiki/faq/cpp11-language#rvalue-refs",
                    "youtube": "https://www.youtube.com/watch?v=IOkgRHmWtE0"
                },
                {
                    "id": max_id + 15,
                    "title": "OOPs: Diamond Problem, Virtual Inheritance & Memory Layout in C++",
                    "difficulty": "Medium",
                    "link": "https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem",
                    "article": "https://www.geeksforgeeks.org/multiple-inheritance-in-c/",
                    "youtube": "https://www.youtube.com/watch?v=Cq_i2Z8W-w0"
                },
                {
                    "id": max_id + 16,
                    "title": "OOPs: Design Patterns for Interviews (Singleton, Factory, Observer & Strategy)",
                    "difficulty": "Hard",
                    "link": "https://refactoring.guru/design-patterns",
                    "article": "https://refactoring.guru/design-patterns/cpp",
                    "youtube": "https://www.youtube.com/watch?v=v9ejT8FO-7I"
                }
            ]
        },
        {
            "subtopic": "Operating Systems (OS) Core Fundamentals",
            "problems": [
                {
                    "id": max_id + 17,
                    "title": "OS: Process vs Thread vs Coroutine (PCB, TCB, Context Switching Costs & Overhead)",
                    "difficulty": "Easy",
                    "link": "https://takeuforward.org/operating-systems/process-vs-thread/",
                    "article": "https://takeuforward.org/operating-systems/process-vs-thread/",
                    "youtube": "https://www.youtube.com/watch?v=OrM7nZcxXZU",
                    "mit": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/"
                },
                {
                    "id": max_id + 18,
                    "title": "OS: Concurrency & Synchronization (Mutex vs Semaphore, Race Conditions & Deadlock Coffman Conditions)",
                    "difficulty": "Medium",
                    "link": "https://takeuforward.org/operating-systems/concurrency-and-synchronization/",
                    "article": "https://takeuforward.org/operating-systems/concurrency-and-synchronization/",
                    "youtube": "https://www.youtube.com/watch?v=ukM_zzrIeXs"
                },
                {
                    "id": max_id + 19,
                    "title": "OS: Virtual Memory, Paging, TLB Cache, Page Faults & LRU Page Replacement",
                    "difficulty": "Medium",
                    "link": "https://takeuforward.org/operating-systems/virtual-memory-and-paging/",
                    "article": "https://takeuforward.org/operating-systems/virtual-memory-and-paging/",
                    "youtube": "https://www.youtube.com/watch?v=2quKg6vQ9rY"
                },
                {
                    "id": max_id + 20,
                    "title": "OS: CPU Scheduling Algorithms (Round Robin, CFS, SJF & Starvation)",
                    "difficulty": "Easy",
                    "link": "https://takeuforward.org/operating-systems/cpu-scheduling-algorithms/",
                    "article": "https://takeuforward.org/operating-systems/cpu-scheduling-algorithms/",
                    "youtube": "https://www.youtube.com/watch?v=EWkvdbyE1gY"
                }
            ]
        },
        {
            "subtopic": "Database Management Systems (DBMS) Internals",
            "problems": [
                {
                    "id": max_id + 21,
                    "title": "DBMS: ACID Properties & Transaction Isolation Levels (Dirty, Non-Repeatable & Phantom Reads)",
                    "difficulty": "Medium",
                    "link": "https://takeuforward.org/dbms/acid-properties-in-dbms/",
                    "article": "https://takeuforward.org/dbms/acid-properties-in-dbms/",
                    "youtube": "https://www.youtube.com/watch?v=gaT_8A6kC_E"
                },
                {
                    "id": max_id + 22,
                    "title": "DBMS: Database Indexing Internals (Why B+ Trees Beat Binary Search Trees & Hash Maps on Disk)",
                    "difficulty": "Hard",
                    "link": "https://en.wikipedia.org/wiki/B%2B_tree",
                    "article": "https://use-the-index-luke.com/",
                    "youtube": "https://www.youtube.com/watch?v=aZjYr87r1b8"
                },
                {
                    "id": max_id + 23,
                    "title": "DBMS: Database Normalization (1NF, 2NF, 3NF, BCNF and Anomaly Elimination)",
                    "difficulty": "Easy",
                    "link": "https://takeuforward.org/dbms/normalization-in-dbms/",
                    "article": "https://takeuforward.org/dbms/normalization-in-dbms/",
                    "youtube": "https://www.youtube.com/watch?v=5fs1PRZzp6k"
                }
            ]
        },
        {
            "subtopic": "Computer Networks (CN) & Internet Protocols",
            "problems": [
                {
                    "id": max_id + 24,
                    "title": "CN: What Happens When You Type google.com in Your Browser (DNS -> TCP -> TLS -> HTTP/3 Flow)",
                    "difficulty": "Medium",
                    "link": "https://github.com/alex/what-happens-when",
                    "article": "https://github.com/alex/what-happens-when",
                    "youtube": "https://www.youtube.com/watch?v=kZX3QvDkM_Y"
                },
                {
                    "id": max_id + 25,
                    "title": "CN: TCP 3-Way Handshake & 4-Way Teardown vs UDP (Flow Control, Congestion Window & Low Latency)",
                    "difficulty": "Medium",
                    "link": "https://takeuforward.org/computer-networks/tcp-3-way-handshake/",
                    "article": "https://takeuforward.org/computer-networks/tcp-3-way-handshake/",
                    "youtube": "https://www.youtube.com/watch?v=F27PLhn3W04"
                },
                {
                    "id": max_id + 26,
                    "title": "CN: HTTP vs HTTPS, SSL/TLS Handshake & Symmetric vs Asymmetric Encryption",
                    "difficulty": "Easy",
                    "link": "https://www.cloudflare.com/learning/ssl/what-is-https/",
                    "article": "https://www.cloudflare.com/learning/ssl/what-is-https/",
                    "youtube": "https://www.youtube.com/watch?v=T4Df5_cojAs"
                }
            ]
        },
        {
            "subtopic": "Low-Level Design (LLD) & Machine Coding Challenges",
            "problems": [
                {
                    "id": max_id + 27,
                    "title": "LLD: Design a Multi-Floor Parking Lot System in C++ (OOP Architecture & Strategy Pattern)",
                    "difficulty": "Medium",
                    "link": "https://github.com/ashishps1/awesome-low-level-design",
                    "article": "https://github.com/ashishps1/awesome-low-level-design",
                    "youtube": "https://www.youtube.com/watch?v=tVRyb4HaHgw"
                },
                {
                    "id": max_id + 28,
                    "title": "LLD: Design an In-Memory Key-Value Store with Transactions (Commit & Rollback)",
                    "difficulty": "Hard",
                    "link": "https://github.com/ashishps1/awesome-low-level-design",
                    "article": "https://github.com/ashishps1/awesome-low-level-design",
                    "youtube": "https://www.youtube.com/watch?v=4Ym8M4y0o78"
                },
                {
                    "id": max_id + 29,
                    "title": "LLD: Design a Rate Limiter (Token Bucket & Leaky Bucket Algorithms in C++)",
                    "difficulty": "Medium",
                    "link": "https://github.com/ashishps1/awesome-low-level-design",
                    "article": "https://en.wikipedia.org/wiki/Token_bucket",
                    "youtube": "https://www.youtube.com/watch?v=CRGPbCbRpHU"
                },
                {
                    "id": max_id + 30,
                    "title": "LLD: Design a Snake and Ladder / Tic-Tac-Toe Game Engine (Modular Extensible Design)",
                    "difficulty": "Easy",
                    "link": "https://github.com/ashishps1/awesome-low-level-design",
                    "article": "https://github.com/ashishps1/awesome-low-level-design",
                    "youtube": "https://www.youtube.com/watch?v=gktZsX9Z_hM"
                },
                {
                    "id": max_id + 31,
                    "title": "LLD: Design a Splitwise Expense Sharing Engine (Equal, Exact & Percent Splits)",
                    "difficulty": "Medium",
                    "link": "https://github.com/ashishps1/awesome-low-level-design",
                    "article": "https://github.com/ashishps1/awesome-low-level-design",
                    "youtube": "https://www.youtube.com/watch?v=ro7CEk3w9e8"
                }
            ]
        }
    ]
}

# Check if step-22 already exists
existing_s22 = False
for i, s in enumerate(data):
    if s['stepId'] == 'step-22':
        data[i] = step_22
        existing_s22 = True
        break

if not existing_s22:
    data.append(step_22)

# Save to data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write("// Striver's A2Z DSA Sheet + Unified NeetCode 150 & Blind 75 Pattern Base + Step 22 Core CS & LLD\n")
    f.write("const DSA_DATA = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = DSA_DATA;\n}\n")

total = sum(len(t['problems']) for s in data for t in s['topics'])
print(f"Successfully added Step 22! Total Steps: {len(data)}, Grand Total Problems/Interview Units: {total}")
