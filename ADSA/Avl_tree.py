class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def height(self, node):
        return 0 if not node else node.height

    def balance(self, node):
        return 0 if not node else self.height(node.left) - self.height(node.right)

    def leftrotate(self, x):
        y = x.right
        t = y.left
        y.left = x
        x.right = t
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def rightrotate(self, y):
        x = y.left
        t = x.right
        x.right = y
        y.left = t
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def insert(self, root, key):
        if not root:
            return Node(key)

        if key < root.data:
            root.left = self.insert(root.left, key)
        elif key > root.data:
            root.right = self.insert(root.right, key)
        else:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        b = self.balance(root)

        if b > 1 and key < root.left.data:
            return self.rightrotate(root)
        if b < -1 and key > root.right.data:
            return self.leftrotate(root)
        if b > 1 and key > root.left.data:
            root.left = self.leftrotate(root.left)
            return self.rightrotate(root)
        if b < -1 and key < root.right.data:
            root.right = self.rightrotate(root.right)
            return self.leftrotate(root)

        return root

    def minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, root, key):
        if not root:
            print("Node not found.")
            return root

        if key < root.data:
            root.left = self.delete(root.left, key)
        elif key > root.data:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            temp = self.minimum(root.right)
            root.data = temp.data
            root.right = self.delete(root.right, temp.data)

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        b = self.balance(root)

        if b > 1 and self.balance(root.left) >= 0:
            return self.rightrotate(root)
        if b > 1 and self.balance(root.left) < 0:
            root.left = self.leftrotate(root.left)
            return self.rightrotate(root)
        if b < -1 and self.balance(root.right) <= 0:
            return self.leftrotate(root)
        if b < -1 and self.balance(root.right) > 0:
            root.right = self.rightrotate(root.right)
            return self.leftrotate(root)

        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.data, end=" ")
            self.inorder(root.right)
tree = AVL()
root = None
print("\n========== AVL TREE OPERATIONS ==========")
while True:
    print("\n1.Insert 2.Delete 3.Inorder 4.Exit")

    ch = int(input("Enter choice: "))
    if ch == 1:
        n = int(input("Enter number of nodes: "))
        for i in range(n):
            root = tree.insert(root, int(input("Enter value: ")))

    elif ch == 2:
        root = tree.delete(root, int(input("Enter value to delete: ")))

    elif ch == 3:
        print("Inorder:", end=" ")
        tree.inorder(root)
        print()

    elif ch == 4:
        print("Program terminated.")
        break

    else:
        print("Invalid choice.")