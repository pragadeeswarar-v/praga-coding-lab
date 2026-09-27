class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent] < self.heap[index]:
                self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
                index = parent
            else:
                break

    def delete(self):
        if len(self.heap) == 0:
            print("Heap is Empty!")
            return

        deleted = self.heap[0]

        if len(self.heap) == 1:
            self.heap.pop()
            print(f"{deleted} deleted successfully!")
            return

        self.heap[0] = self.heap.pop()
        self.heapify_down(0)

        print(f"{deleted} deleted successfully!")

    def heapify_down(self, index):
        size = len(self.heap)

        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and self.heap[left] > self.heap[largest]:
                largest = left

            if right < size and self.heap[right] > self.heap[largest]:
                largest = right

            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break

    def display(self):
        if len(self.heap) == 0:
            print("Heap is Empty!")
        else:
            print("Heap Elements:", self.heap)

    def heap_sort(self):
        if len(self.heap) == 0:
            print("Heap is Empty!")
            return

        temp = self.heap.copy()
        result = []

        while len(self.heap) > 0:
            result.append(self.heap[0])

            if len(self.heap) == 1:
                self.heap.pop()
            else:
                self.heap[0] = self.heap.pop()
                self.heapify_down(0)

        print("Heap Sort (Descending):", result)
        self.heap = temp


def main():
    h = MaxHeap()

    while True:
        print("\n==========================")
        print("      HEAP OPERATIONS")
        print("==========================")
        print("1. Insert")
        print("2. Delete Root")
        print("3. Display")
        print("4. Heap Sort")
        print("5. Exit")
        print("==========================")

        ch = input("Enter choice: ")

        if ch == "1":
            try:
                val = int(input("Enter value to insert: "))
                h.insert(val)
                print(f"{val} inserted successfully!")
            except ValueError:
                print("Invalid Input!")

        elif ch == "2":
            h.delete()

        elif ch == "3":
            h.display()

        elif ch == "4":
            h.heap_sort()

        elif ch == "5":
            print("Exiting Program...")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()