class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    def traverse(self):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].traverse()
            print(self.keys[i], end=" ")
        if not self.leaf:
            self.children[len(self.keys)].traverse()

    def search(self, k):
        i = 0
        while i < len(self.keys) and k > self.keys[i]:
            i += 1

        if i < len(self.keys) and self.keys[i] == k:
            return self, i

        if self.leaf:
            return None

        return self.children[i].search(k)

    def insert_non_full(self, k):
        i = len(self.keys) - 1

        if self.leaf:
            self.keys.append(None)
            while i >= 0 and self.keys[i] > k:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
        else:
            while i >= 0 and self.keys[i] > k:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i, self.children[i])
                if self.keys[i] < k:
                    i += 1
            self.children[i].insert_non_full(k)

    def split_child(self, i, y):
        t = self.t
        z = BTreeNode(t, y.leaf)

        z.keys = y.keys[t:]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        key_to_move = y.keys[t - 1]
        y.keys = y.keys[:t - 1]

        self.children.insert(i + 1, z)
        self.keys.insert(i, key_to_move)

    def find_key(self, k):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < k:
            idx += 1
        return idx

    def delete(self, k):
        idx = self.find_key(k)

        if idx < len(self.keys) and self.keys[idx] == k:
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            if self.leaf:
                print(f"Key {k} not found in the tree.")
                return

            flag = (idx == len(self.keys))

            if len(self.children[idx].keys) < self.t:
                self.fill(idx)

            if flag and idx > len(self.keys):
                self.children[idx - 1].delete(k)
            else:
                self.children[idx].delete(k)

    def remove_from_leaf(self, idx):
        self.keys.pop(idx)

    def remove_from_non_leaf(self, idx):
        k = self.keys[idx]

        if len(self.children[idx].keys) >= self.t:
            pred = self.get_predecessor(idx)
            self.keys[idx] = pred
            self.children[idx].delete(pred)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ = self.get_successor(idx)
            self.keys[idx] = succ
            self.children[idx + 1].delete(succ)
        else:
            self.merge(idx)
            self.children[idx].delete(k)

    def get_predecessor(self, idx):
        cur = self.children[idx]
        while not cur.leaf:
            cur = cur.children[len(cur.keys)]
        return cur.keys[-1]

    def get_successor(self, idx):
        cur = self.children[idx + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]

        child.keys.insert(0, self.keys[idx - 1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop(-1))

        self.keys[idx - 1] = sibling.keys.pop(-1)

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys.pop(idx))
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        self.children.pop(idx + 1)


class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t

    def traverse(self):
        if self.root is not None:
            self.root.traverse()
            print()
        else:
            print("Tree is empty.")

    def search(self, k):
        if self.root is None:
            return None
        return self.root.search(k)

    def insert(self, k):
        if self.root is None:
            self.root = BTreeNode(self.t, True)
            self.root.keys.append(k)
        else:
            if len(self.root.keys) == 2 * self.t - 1:
                s = BTreeNode(self.t, False)
                s.children.append(self.root)
                s.split_child(0, self.root)

                i = 0
                if s.keys[0] < k:
                    i += 1
                s.children[i].insert_non_full(k)
                self.root = s
            else:
                self.root.insert_non_full(k)

    def delete(self, k):
        if not self.root:
            print("Tree is empty.")
            return

        self.root.delete(k)

        if len(self.root.keys) == 0:
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]


def get_valid_number(prompt):
    while True:
        inp = input(prompt).strip()
        if inp.isdigit() or (inp.startswith('-') and inp[1:].isdigit()):
            return int(inp)
        print("Please enter a valid integer.")


def main():
    while True:
        t = get_valid_number("Enter minimum degree (t >= 2): ")
        if t >= 2:
            break
        print("Minimum degree must be at least 2.")

    btree = BTree(t)

    while True:
        print("\n--- B-TREE MENU ---")
        print("1. Insert")
        print("2. Search")
        print("3. Delete")
        print("4. Inorder Traversal")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            count = get_valid_number("How many elements do you want to insert? ")
            for i in range(count):
                val = get_valid_number(f"Enter key {i + 1}: ")
                btree.insert(val)
                print(f"Key {val} inserted successfully.")

        elif choice == "2":
            val = get_valid_number("Enter key to search: ")
            res = btree.search(val)
            if res:
                print(f"Key {val} found in tree.")
            else:
                print(f"Key {val} not found in tree.")

        elif choice == "3":
            val = get_valid_number("Enter key to delete: ")
            if btree.search(val):
                btree.delete(val)
                print(f"Key {val} deleted successfully.")
            else:
                print(f"Key {val} not found in tree.")

        elif choice == "4":
            print("Inorder Traversal: ", end="")
            btree.traverse()

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    main()