class Node:
    def __init__(self, data: int):
        self.data = data
        self.left = None
        self.right = None


class BinTree:
    def __init__(self):
        self.root = None

    def init_with_tree(self, tree: Node):
        '''Inicjalizuje drzewo z danymi
        tree - drzewo do inicjalizacji (Node)
        '''
        if tree is None:
            print("Empty tree")
            return
        self.root = tree  

    def print_tree(self):
        '''Proste BFS
        Wypisywanie drzewa uzywając kolejki do przeszukiwania kolejnych poziomów drzewa
        '''
        if self.root is None:
            return
        q = [self.root]

        while len(q) > 0:
            level = len(q)
            for _ in range(level):
                node = q.pop(0)
                print(node.data, end=" ")
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
            print()

    # Poniższe funkcje nie są potrzebna do wykonania zadania, ale ułatwiają pracę z danymi i testowanie
    # ---------------------------------------------------------------------------------------------------------
    def insert(self, data: int):
        '''Dodaje dany element do drzewa
        data - dane do dodania (int)
        '''
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(self.root, data)

    def _insert_node(self, node: Node, data: int):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_node(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_node(node.right, data)
    # ---------------------------------------------------------------------------------------------------------
            
    

if __name__ == "__main__":
    tree = BinTree()

    # Testowanie dla drzewa z zadania
    tree_base = Node(1)
    tree_base.left = Node(2)
    tree_base.right = Node(3)
    tree_base.left.left = Node(4)
    tree_base.right.left = Node(5)
    tree_base.right.right = Node(6)

    tree.init_with_tree(tree_base)

    tree.print_tree()