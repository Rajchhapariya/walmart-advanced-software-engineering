import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class PowerOfTwoMaxHeap {

    private final int childExponent;
    private final int branchingFactor;
    private int[] heap;
    private int size;

    public PowerOfTwoMaxHeap(int childExponent) {
        this(childExponent, 16);
    }

    public PowerOfTwoMaxHeap(int childExponent, int initialCapacity) {
        if (childExponent < 0) {
            throw new IllegalArgumentException("Exponent must be non-negative: " + childExponent);
        }
        if (initialCapacity <= 0) {
            throw new IllegalArgumentException("Initial capacity must be positive: " + initialCapacity);
        }

        this.childExponent = childExponent;
        // if exponent >= 30, 2^x exceeds 32-bit int bounds, so clamp to prevent negative shift wrap
        this.branchingFactor = (childExponent >= 30) ? Integer.MAX_VALUE : (1 << childExponent);
        this.heap = new int[initialCapacity];
        this.size = 0;
    }

    public void insert(int value) {
        ensureCapacity(size + 1);
        heap[size] = value;
        siftUp(size);
        size++;
    }

    public int popMax() {
        if (size == 0) {
            throw new IllegalStateException("Heap is empty");
        }

        int max = heap[0];
        int last = heap[size - 1];
        size--;

        if (size > 0) {
            siftDown(0, last);
        }

        return max;
    }

    public int peekMax() {
        if (size == 0) {
            throw new IllegalStateException("Heap is empty");
        }
        return heap[0];
    }

    public int peek() {
        return peekMax();
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void clear() {
        size = 0;
    }

    public int getChildExponent() {
        return childExponent;
    }

    public int[] toArray() {
        return Arrays.copyOf(heap, size);
    }

    public List<Integer> getHeap() {
        List<Integer> list = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            list.add(heap[i]);
        }
        return list;
    }

    // bubble up using hole percolation to avoid 3-way swap overhead
    private void siftUp(int index) {
        int target = heap[index];

        while (index > 0) {
            int parentIndex = getParentIndex(index);
            if (target > heap[parentIndex]) {
                heap[index] = heap[parentIndex];
                index = parentIndex;
            } else {
                break;
            }
        }

        heap[index] = target;
    }

    // push down by finding the largest among all 2^childExponent children
    private void siftDown(int index, int target) {
        while (true) {
            long firstChildLong = getFirstChildIndexLong(index);

            // no children left
            if (firstChildLong >= size) {
                break;
            }

            int firstChild = (int) firstChildLong;
            int lastChild;

            if (childExponent >= 30) {
                lastChild = size;
            } else {
                long lastChildLong = firstChildLong + branchingFactor;
                lastChild = (int) Math.min(lastChildLong, (long) size);
            }

            // scan children to find max child
            int bestChildIndex = firstChild;
            int bestChildValue = heap[firstChild];

            for (int c = firstChild + 1; c < lastChild; c++) {
                if (heap[c] > bestChildValue) {
                    bestChildValue = heap[c];
                    bestChildIndex = c;
                }
            }

            // if largest child is bigger than target, promote child into hole
            if (bestChildValue > target) {
                heap[index] = bestChildValue;
                index = bestChildIndex;
            } else {
                break;
            }
        }

        heap[index] = target;
    }

    // parent index = (child - 1) / (2^k) -> (child - 1) >>> k
    private int getParentIndex(int childIndex) {
        if (childExponent >= 30) {
            return 0; // for x >= 30, all elements are direct children of root
        }
        return (childIndex - 1) >>> childExponent;
    }

    // first child index = (parent * 2^k) + 1
    private long getFirstChildIndexLong(int parentIndex) {
        if (childExponent >= 30) {
            return (parentIndex == 0) ? 1L : Long.MAX_VALUE;
        }
        return (((long) parentIndex) << childExponent) + 1L;
    }

    private void ensureCapacity(int minCapacity) {
        if (minCapacity > heap.length) {
            int newCapacity = heap.length * 2;
            if (newCapacity < minCapacity) {
                newCapacity = minCapacity;
            }
            heap = Arrays.copyOf(heap, newCapacity);
        }
    }

    public static void main(String[] args) {
        System.out.println("PowerOfTwoMaxHeap Execution Demo");
        System.out.println("================================");

        // Demo 1: 4-ary heap (x = 2, 4 children per parent)
        int childExponent = 2;
        System.out.println("\n1. Initializing heap with childExponent = " + childExponent + " (4 children/parent):");
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(childExponent);

        int[] sampleData = {15, 3, 29, 44, 8, 12, 50, 7, 33, 19, 2};
        System.out.print("Inserting values: ");
        for (int v : sampleData) {
            System.out.print(v + " ");
            heap.insert(v);
        }
        System.out.println();

        System.out.println("Heap size: " + heap.size());
        System.out.println("Max element (peek): " + heap.peekMax());
        System.out.print("Popping elements in order: ");
        while (!heap.isEmpty()) {
            System.out.print(heap.popMax() + " ");
        }
        System.out.println();

        // Demo 2: Boundary test with small exponent (x = 0, unary heap)
        System.out.println("\n2. Boundary test with childExponent = 0 (unary chain, 1 child/parent):");
        PowerOfTwoMaxHeap unaryHeap = new PowerOfTwoMaxHeap(0);
        int[] unaryData = {10, 40, 20, 50, 30};
        for (int v : unaryData) unaryHeap.insert(v);
        System.out.print("Popping from unary heap: ");
        while (!unaryHeap.isEmpty()) {
            System.out.print(unaryHeap.popMax() + " ");
        }
        System.out.println();

        // Demo 3: Boundary test with large exponent (x = 30)
        System.out.println("\n3. Boundary test with childExponent = 30 (all children under root):");
        PowerOfTwoMaxHeap largeHeap = new PowerOfTwoMaxHeap(30);
        int[] largeData = {100, 25, 300, 42, 500};
        for (int v : largeData) largeHeap.insert(v);
        System.out.print("Popping from large exponent heap: ");
        while (!largeHeap.isEmpty()) {
            System.out.print(largeHeap.popMax() + " ");
        }
        System.out.println();

        System.out.println("\nExecution completed successfully.");
    }
}
