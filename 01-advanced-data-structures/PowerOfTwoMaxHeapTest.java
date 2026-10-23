import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 * Test suite for PowerOfTwoMaxHeap covering:
 * - Very small exponents (x = 0, unary heap)
 * - Standard exponents (x = 1, binary heap; x = 2, 4-ary heap; x = 3, 8-ary heap)
 * - Large exponents (x = 10, 1024-ary heap; x = 30; x = 31; x = 100)
 * - Sneaky edge cases: empty heap pop/peek, negative exponent, non-positive capacity,
 *   single element, duplicate elements, reverse sorted input, stress test with 50,000 items.
 */
public class PowerOfTwoMaxHeapTest {

    private static int testsPassed = 0;
    private static int testsTotal = 0;

    public static void main(String[] args) {
        System.out.println("Starting PowerOfTwoMaxHeap Test Suite...\n");

        testConstructorValidation();
        testSmallExponentZero();
        testBinaryHeapExponentOne();
        testFourAryHeapExponentTwo();
        testEightAryHeapExponentThree();
        testLargeExponentThirtyAndAbove();
        testDuplicateValues();
        testEmptyHeapExceptions();
        testStressRandomCorrectness();
        testPerformanceComparison();

        System.out.println(String.format("\nTest Summary: %d/%d tests passed.", testsPassed, testsTotal));
        if (testsPassed == testsTotal) {
            System.out.println("ALL TESTS PASSED SUCCESSFULLY.");
        } else {
            System.err.println("SOME TESTS FAILED.");
            System.exit(1);
        }
    }

    private static void assertTrue(boolean condition, String testName) {
        testsTotal++;
        if (condition) {
            testsPassed++;
            System.out.println("[PASS] " + testName);
        } else {
            System.err.println("[FAIL] " + testName);
            new Exception("Assertion failure").printStackTrace(System.err);
        }
    }

    private static void assertEquals(int expected, int actual, String testName) {
        testsTotal++;
        if (expected == actual) {
            testsPassed++;
            System.out.println("[PASS] " + testName);
        } else {
            System.err.println(String.format("[FAIL] %s - Expected: %d, Actual: %d", testName, expected, actual));
        }
    }

    // Constructor parameter validation
    private static void testConstructorValidation() {
        boolean caughtNegativeExp = false;
        try {
            new PowerOfTwoMaxHeap(-1);
        } catch (IllegalArgumentException e) {
            caughtNegativeExp = true;
        }
        assertTrue(caughtNegativeExp, "Negative child exponent should throw IllegalArgumentException");

        boolean caughtInvalidCap = false;
        try {
            new PowerOfTwoMaxHeap(2, 0);
        } catch (IllegalArgumentException e) {
            caughtInvalidCap = true;
        }
        assertTrue(caughtInvalidCap, "Non-positive capacity should throw IllegalArgumentException");
    }

    // Degree x = 0 (2^0 = 1 child per parent: unary linear chain)
    private static void testSmallExponentZero() {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(0);
        int[] values = {10, 40, 20, 50, 30};
        for (int v : values) {
            heap.insert(v);
        }

        assertEquals(5, heap.size(), "Size should be 5 for x=0");
        assertEquals(50, heap.peek(), "Max should be 50 for x=0");

        // Popping all should return in non-increasing order: 50, 40, 30, 20, 10
        int prev = Integer.MAX_VALUE;
        while (!heap.isEmpty()) {
            int current = heap.popMax();
            assertTrue(current <= prev, "Popped values must be non-increasing for x=0: " + current);
            prev = current;
        }
        assertEquals(10, prev, "Last popped element should be 10 for x=0");
    }

    // Degree x = 1 (2^1 = 2 children: standard binary max heap)
    private static void testBinaryHeapExponentOne() {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(1);
        int[] values = {15, 10, 20, 8, 12, 25, 30, 5};
        for (int v : values) {
            heap.insert(v);
        }

        assertEquals(8, heap.size(), "Size should be 8 for x=1");
        assertEquals(30, heap.peekMax(), "Root should be 30 for x=1");

        int[] expectedPopped = {30, 25, 20, 15, 12, 10, 8, 5};
        for (int exp : expectedPopped) {
            assertEquals(exp, heap.popMax(), "PopMax should return next largest for x=1");
        }
        assertTrue(heap.isEmpty(), "Heap should be empty after popping all elements");
    }

    // Degree x = 2 (2^2 = 4 children: 4-ary heap)
    private static void testFourAryHeapExponentTwo() {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(2);
        int[] values = {3, 9, 1, 14, 27, 8, 19, 35, 2, 44, 11};
        for (int v : values) {
            heap.insert(v);
        }

        assertEquals(44, heap.peekMax(), "Root must be 44 for x=2");

        int prev = Integer.MAX_VALUE;
        int count = 0;
        while (!heap.isEmpty()) {
            int cur = heap.popMax();
            assertTrue(cur <= prev, "Popped values must be non-increasing for x=2: " + cur);
            prev = cur;
            count++;
        }
        assertEquals(values.length, count, "All elements popped for x=2");
    }

    // Degree x = 3 (2^3 = 8 children: 8-ary heap)
    private static void testEightAryHeapExponentThree() {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(3);
        int[] values = {100, 25, 300, 42, 500, 12, 85, 99, 1000, 7, 55, 60, 70, 80, 90, 95, 110};
        for (int v : values) {
            heap.insert(v);
        }

        assertEquals(1000, heap.popMax(), "First pop must be 1000 for x=3");
        assertEquals(500, heap.popMax(), "Second pop must be 500 for x=3");
        assertEquals(300, heap.popMax(), "Third pop must be 300 for x=3");
    }

    // Edge case: Large exponents (x >= 30, x = 31, x = 100)
    private static void testLargeExponentThirtyAndAbove() {
        int[] largeExponents = {30, 31, 32, 100};
        for (int exp : largeExponents) {
            PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(exp);
            int[] values = {45, 12, 89, 3, 999, 234, 1, 550};
            for (int v : values) {
                heap.insert(v);
            }

            assertEquals(values.length, heap.size(), "Size match for exponent=" + exp);
            assertEquals(999, heap.peekMax(), "Max must be 999 for exponent=" + exp);

            int prev = Integer.MAX_VALUE;
            while (!heap.isEmpty()) {
                int cur = heap.popMax();
                assertTrue(cur <= prev, "Popped values must be non-increasing for exponent=" + exp);
                prev = cur;
            }
        }
    }

    // Duplicate values and signed integers
    private static void testDuplicateValues() {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(2);
        int[] values = {7, -5, 7, 10, -5, 0, 7, 10, -20};
        for (int v : values) {
            heap.insert(v);
        }

        assertEquals(10, heap.popMax(), "Duplicate test pop 1");
        assertEquals(10, heap.popMax(), "Duplicate test pop 2");
        assertEquals(7, heap.popMax(), "Duplicate test pop 3");
        assertEquals(7, heap.popMax(), "Duplicate test pop 4");
        assertEquals(7, heap.popMax(), "Duplicate test pop 5");
        assertEquals(0, heap.popMax(), "Duplicate test pop 6");
        assertEquals(-5, heap.popMax(), "Duplicate test pop 7");
        assertEquals(-5, heap.popMax(), "Duplicate test pop 8");
        assertEquals(-20, heap.popMax(), "Duplicate test pop 9");
        assertTrue(heap.isEmpty(), "Heap should be empty after duplicates popped");
    }

    // Exception handling on empty heap
    private static void testEmptyHeapExceptions() {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(1);
        boolean caughtPop = false;
        try {
            heap.popMax();
        } catch (IllegalStateException e) {
            caughtPop = true;
        }
        assertTrue(caughtPop, "Empty popMax should throw IllegalStateException");

        boolean caughtPeek = false;
        try {
            heap.peek();
        } catch (IllegalStateException e) {
            caughtPeek = true;
        }
        assertTrue(caughtPeek, "Empty peek should throw IllegalStateException");
    }

    // Randomized stress test: 50,000 operations across branching factors
    private static void testStressRandomCorrectness() {
        int[] exponentsToTest = {0, 1, 2, 4, 8, 30};
        Random rng = new Random(42);

        for (int exp : exponentsToTest) {
            PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(exp);
            List<Integer> expectedList = new ArrayList<>();

            int numElements = 20000;
            for (int i = 0; i < numElements; i++) {
                int val = rng.nextInt(200000) - 100000;
                heap.insert(val);
                expectedList.add(val);
            }

            expectedList.sort(Collections.reverseOrder());

            boolean strictlySorted = true;
            for (int i = 0; i < numElements; i++) {
                int actual = heap.popMax();
                if (actual != expectedList.get(i)) {
                    strictlySorted = false;
                    break;
                }
            }

            assertTrue(strictlySorted, String.format("Stress sort match for 20,000 elements with exponent %d", exp));
            assertTrue(heap.isEmpty(), "Heap empty after stress test for exponent " + exp);
        }
    }

    // Empirical throughput and latency benchmark
    private static void testPerformanceComparison() {
        int operations = 100000;
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(3); // 8-ary heap
        Random rng = new Random(12345);

        long startInsert = System.nanoTime();
        for (int i = 0; i < operations; i++) {
            heap.insert(rng.nextInt());
        }
        long endInsert = System.nanoTime();

        long startPop = System.nanoTime();
        while (!heap.isEmpty()) {
            heap.popMax();
        }
        long endPop = System.nanoTime();

        double insertMs = (endInsert - startInsert) / 1_000_000.0;
        double popMs = (endPop - startPop) / 1_000_000.0;

        System.out.println(String.format("Performance (100k ops, x=3): Insert=%.2f ms, PopMax=%.2f ms", insertMs, popMs));
        assertTrue(heap.isEmpty(), "Heap empty after benchmark");
    }
}
