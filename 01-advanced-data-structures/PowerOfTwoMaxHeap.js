class PowerOfTwoMaxHeap {
  constructor(childExponent, initialCapacity = 16) {
    if (childExponent < 0) {
      throw new Error(`Exponent must be non-negative: ${childExponent}`);
    }
    if (initialCapacity <= 0) {
      throw new Error(`Initial capacity must be positive: ${initialCapacity}`);
    }

    this.childExponent = childExponent;
    // in JS, bitwise shifts wrap at 32 bits, clamp for exponent >= 30
    this.branchingFactor =
      childExponent >= 30 ? Number.MAX_SAFE_INTEGER : 1 << childExponent;
    this.heap = [];
  }

  insert(value) {
    this.heap.push(value);
    this._siftUp(this.heap.length - 1);
  }

  popMax() {
    if (this.heap.length === 0) {
      throw new Error("Heap is empty");
    }

    const max = this.heap[0];
    const last = this.heap.pop();

    if (this.heap.length > 0) {
      this.heap[0] = last;
      this._siftDown(0);
    }

    return max;
  }

  peekMax() {
    if (this.heap.length === 0) {
      throw new Error("Heap is empty");
    }
    return this.heap[0];
  }

  peek() {
    return this.peekMax();
  }

  size() {
    return this.heap.length;
  }

  isEmpty() {
    return this.heap.length === 0;
  }

  clear() {
    this.heap = [];
  }

  getChildExponent() {
    return this.childExponent;
  }

  toArray() {
    return [...this.heap];
  }

  getHeap() {
    return [...this.heap];
  }

  _siftUp(index) {
    const target = this.heap[index];

    while (index > 0) {
      const parentIndex = this._getParentIndex(index);
      if (target > this.heap[parentIndex]) {
        this.heap[index] = this.heap[parentIndex];
        index = parentIndex;
      } else {
        break;
      }
    }

    this.heap[index] = target;
  }

  _siftDown(index) {
    const target = this.heap[index];
    const size = this.heap.length;

    while (true) {
      const firstChild = this._getFirstChildIndex(index);

      if (firstChild >= size) {
        break;
      }

      let lastChild;
      if (this.childExponent >= 30) {
        lastChild = size;
      } else {
        lastChild = Math.min(firstChild + this.branchingFactor, size);
      }

      let bestChildIndex = firstChild;
      let bestChildValue = this.heap[firstChild];

      for (let c = firstChild + 1; c < lastChild; c++) {
        if (this.heap[c] > bestChildValue) {
          bestChildValue = this.heap[c];
          bestChildIndex = c;
        }
      }

      if (bestChildValue > target) {
        this.heap[index] = bestChildValue;
        index = bestChildIndex;
      } else {
        break;
      }
    }

    this.heap[index] = target;
  }

  _getParentIndex(childIndex) {
    if (this.childExponent >= 30) {
      return 0;
    }
    return Math.floor((childIndex - 1) / (1 << this.childExponent));
  }

  _getFirstChildIndex(parentIndex) {
    if (this.childExponent >= 30) {
      return parentIndex === 0 ? 1 : Number.MAX_SAFE_INTEGER;
    }
    return parentIndex * this.branchingFactor + 1;
  }
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = PowerOfTwoMaxHeap;
}
