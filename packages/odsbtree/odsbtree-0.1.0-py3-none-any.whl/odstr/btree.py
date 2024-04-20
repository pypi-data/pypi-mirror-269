class Node:
    def __init__(self, is_leaf=True, keys=None, children=None):
        self.is_leaf = is_leaf
        self.keys = keys or []
        self.children = children or []

class BPlusTree:
    def __init__(self, degree):
        self.root = Node()
        self.degree = degree

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.degree) - 1:
            new_node = Node(is_leaf=False, children=[self.root])
            self.split_child(new_node, 0)
            self.insert_non_full(new_node, key)
            self.root = new_node
        else:
            self.insert_non_full(root, key)

    def split_child(self, parent, index):
        node_to_split = parent.children[index]
        new_node = Node(is_leaf=node_to_split.is_leaf)
        mid_index = self.degree - 1
        
        new_node.keys = node_to_split.keys[mid_index + 1:]
        node_to_split.keys = node_to_split.keys[:mid_index]

        if not node_to_split.is_leaf:
            new_node.children = node_to_split.children[mid_index + 1:]
            node_to_split.children = node_to_split.children[:mid_index + 1]

        parent.keys.insert(index, new_node.keys[0])
        parent.children.insert(index + 1, new_node)

    def insert_non_full(self, node, key):
        if node.is_leaf:
            index = 0
            while index < len(node.keys) and node.keys[index] < key:
                index += 1
            node.keys.insert(index, key)
        else:
            index = len(node.keys) - 1
            while index >= 0 and node.keys[index] > key:
                index -= 1
            index += 1
            
            if len(node.children[index].keys) == (2 * self.degree) - 1:
                self.split_child(node, index)
                if key > node.keys[index]:
                    index += 1
            self.insert_non_full(node.children[index], key)

    def search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return True
        elif node.is_leaf:
            return False
        else:
            return self.search(node.children[i], key)

### 测试B+树实现

if __name__ == "__main__":
    bpt = BPlusTree(degree=3)
    keys_to_insert = [1, 4, 7, 10, 17, 21, 31, 25, 19, 20, 28, 42]
    for key in keys_to_insert:
        bpt.insert(key)

    print("Search for key 10:", bpt.search(bpt.root, 10))
    print("Search for key 22:", bpt.search(bpt.root, 22))