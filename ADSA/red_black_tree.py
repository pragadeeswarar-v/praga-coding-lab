class Node:
    def __init__(self, key, color="RED"):
        self.key = key
        self.color = color  # "RED" or "BLACK"
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        # Sentinel NIL node representing leaves and empty links
        self.NIL = Node(key=0, color="BLACK")
        self.root = self.NIL

    # --- 1. ROTATIONS ---

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    # --- 2. SEARCH ---

    def search_rbt(self, node, key):
        if node == self.NIL or key == node.key:
            return node
        if key < node.key:
            return self.search_rbt(node.left, key)
        return self.search_rbt(node.right, key)

    # --- 3. INSERTION ---

    def insert_rbt(self, key):
        # Standard BST Insert setup
        z = Node(key=key, color="RED")
        z.left = self.NIL
        z.right = self.NIL

        y = self.NIL
        x = self.root

        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        # Fix Red-Black Violations
        self._fix_insert(z)

    def _fix_insert(self, z):
        while z != self.root and z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right

                # Case 1: Uncle is RED -> Recolor
                if uncle.color == "RED":
                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    # Case 2: Triangle shape -> Left Rotate
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)

                    # Case 3: Line shape -> Right Rotate
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                # Symmetric cases (Left <-> Right)
                uncle = z.parent.parent.left

                # Case 1: Uncle is RED
                if uncle.color == "RED":
                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    # Case 2: Triangle shape -> Right Rotate
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)

                    # Case 3: Line shape -> Left Rotate
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)

        self.root.color = "BLACK"

    # --- 4. DELETION ---

    def _transplant(self, u, v):
        """Helper to replace subtree rooted at u with subtree rooted at v."""
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _min_value_node(self, node):
        current = node
        while current.left != self.NIL:
            current = current.left
        return current

    def delete_rbt(self, key):
        z = self.search_rbt(self.root, key)
        if z == self.NIL:
            print(f"Key {key} not found in tree.")
            return

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._min_value_node(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                sibling = x.parent.right

                # Case 1: Sibling is RED
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    sibling = x.parent.right

                # Case 2: Sibling's children are both BLACK
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    sibling.color = "RED"
                    x = x.parent
                else:
                    # Case 3: Sibling's right child is BLACK, left is RED
                    if sibling.right.color == "BLACK":
                        sibling.left.color = "BLACK"
                        sibling.color = "RED"
                        self.right_rotate(sibling)
                        sibling = x.parent.right

                    # Case 4: Sibling's right child is RED
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # Symmetric cases (Left <-> Right)
                sibling = x.parent.left

                # Case 1: Sibling is RED
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    sibling = x.parent.left

                # Case 2: Sibling's children are both BLACK
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    sibling.color = "RED"
                    x = x.parent
                else:
                    # Case 3: Sibling's left child is BLACK, right is RED
                    if sibling.left.color == "BLACK":
                        sibling.right.color = "BLACK"
                        sibling.color = "RED"
                        self.left_rotate(sibling)
                        sibling = x.parent.left

                    # Case 4: Sibling's left child is RED
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "BLACK"
    def print_tree(self, node=None, indent="", last=True):
        """Helper to visual printing of the tree layout."""
        if node is None:
            node = self.root

        if node != self.NIL:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "   "
            else:
                print("L----", end="")
                indent += "|  "

            print(f"{node.key} ({node.color})")
            self.print_tree(node.left, indent, False)
            self.print_tree(node.right, indent, True)
if __name__ == "__main__":
    rbt = RedBlackTree()

    # Insert sequence
    keys = [10, 20, 30, 15, 25, 5, 1]
    print("--- Inserting Keys ---")
    for key in keys:
        rbt.insert_rbt(key)

    print("\nTree Structure after Insertions:")
    rbt.print_tree()

    # Search
    print("\n--- Searching Keys ---")
    search_key = 15
    res = rbt.search_rbt(rbt.root, search_key)
    if res != rbt.NIL:
        print(f"Found node with key {search_key}! Color: {res.color}")
    else:
        print(f"Key {search_key} not found.")

    # Deletion
    print("\n--- Deleting Node (20) ---")
    rbt.delete_rbt(20)
    print("Tree Structure after Deleting 20:")
    rbt.print_tree()
