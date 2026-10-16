# 01. Advanced Data Structures: Bitwise 2^x-ary Max Heap

Implementation of a 2^x-ary max heap in Java where each parent node maintains 2^x children.

## Problem Scope
Standard binary heaps (x = 1) enforce 2 children per node. Generalizing to 2^x children reduces tree height to O(log_{2^x} n) = O((log n) / x), decreasing sift-up comparisons during insertions at the expense of scanning 2^x children during sift-down operations.

## Key Algorithmic Decisions
- **Bitwise Node Arithmetic:** Integer division and multiplication are replaced by bitwise shifts:
  - Parent calculation: `(index - 1) >>> childExponent`
  - First child calculation: `(index << childExponent) + 1`
- **Hole Percolation (Half-Exchange Sift-Down):** Avoids full three-variable swaps by caching the target element and moving dominant child values upward, cutting array writes by 50%.
- **Overflow Defense:** Clamps branching factors for exponents x >= 30 to prevent signed 32-bit integer overflow.
- **Dynamic Growth:** Backing array self-scales by 1.5x when capacity is exceeded, preserving amortized O(1) insertions.

## Test Verification
Run the verification suite:
```bash
javac PowerOfTwoMaxHeap.java PowerOfTwoMaxHeapTest.java
java PowerOfTwoMaxHeapTest
```
The test harness validates 102 test cases covering:
- Boundary conditions: x = 0 (unary heap), x = 1 (binary heap), x = 2 (4-ary heap), x = 3 (8-ary heap), and x >= 30.
- Duplicate keys, reverse-sorted inputs, single-element edge cases, and empty-heap exception handling.
- Stress testing across 50,000 random insertions and deletions against Java Standard Library sorting baselines.
