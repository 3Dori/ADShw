from collections import namedtuple
Path = namedtuple('Path', ['tree', 'direction'])
NodeWithDepth = namedtuple('NodeWithDepth', ['tree', 'depth'])

class Tree(object):
    def __init__(self, key=None, copyfrom=None):
        if copyfrom:
            self.key = copyfrom.key
            self.height = copyfrom.height
            self.left = copyfrom.left
            self.right = copyfrom.right
        else:
            self.key = key
            self.height = 1
            self.left = None
            self.right = None

    def insert(self, node):

        node_path = []
        T = self
        while T != None:
            if node.key < T.key:
                node_path.append(Path(T, 'l'))    # node_path record tree in path and direction
                T = T.left
            elif node.key > T.key:
                node_path.append(Path(T, 'r'))
                T = T.right
            else:
                return    # node exist

        parent = node_path.pop()
        last_direction = parent.direction
        if last_direction == 'l':
            parent.tree.left = node
        elif last_direction == 'r':
            parent.tree.right = node
        parent.tree.height = max(parent.tree.get_hl(), parent.tree.get_hr()) + 1

        while node_path:    # a nonrecursive avl tree
            parent = node_path.pop()
            parent.tree.height = max(parent.tree.get_hl(), parent.tree.get_hr()) + 1
            balance = parent.tree.get_balance()
            if balance < -1:
                if last_direction == 'r':    # RR insertion
                    parent.tree.right_rotation()
                elif last_direction == 'l':    # RL insertion
                    parent.tree.right.left_rotation()
                    parent.tree.right_rotation()
            elif balance > 1:
                if last_direction == 'l':    # LL insertion
                    parent.tree.left_rotation()
                elif last_direction == 'r':    # LR insertion
                    parent.tree.left.right_rotation()
                    parent.tree.left_rotation()
            last_direction = parent.direction

    def copy(self, other):
        self.key = other.key
        self.height = other.height
        self.left = other.left
        self.right = other.right

    def left_rotation(self):
        new_node = Tree(copyfrom=self)
        left = self.left
        new_node.height = max(left.get_hr(), new_node.get_hr()) + 1
        left.height = max(left.get_hl(), new_node.height) + 1
        new_node.left = left.right
        left.right = new_node
        self.copy(left)

    def right_rotation(self):
        new_node = Tree(copyfrom=self)
        right = self.right
        new_node.height = max(right.get_hl(), new_node.get_hl()) + 1
        right.height = max(right.get_hr(), new_node.height) + 1
        new_node.right = right.left
        right.left = new_node
        self.copy(right)

    def get_balance(self):
        return self.get_hl() - self.get_hr()

    def get_hl(self):
        if self.left:
            return self.left.height
        else:
            return 0

    def get_hr(self):
        if self.right:
            return self.right.height
        else:
            return 0

    def print_tree(self):
        node_stack = []
        node_stack.append(NodeWithDepth(self, 0))
        while node_stack:
            current_node = node_stack.pop()
            if current_node.tree.right:
                node_stack.append(NodeWithDepth(current_node.tree.right, current_node.depth + 1))
            if current_node.tree.left:
                node_stack.append(NodeWithDepth(current_node.tree.left, current_node.depth + 1))
            print(' ' * current_node.depth + str(current_node.tree.key))

def main():
    T = None
    nodes_to_insert = map(int, input().split())
    for key in nodes_to_insert:
        if T == None:
            T = Tree(key)
        else:
            new_node = Tree(key)
            T.insert(new_node)
    T.print_tree()

if __name__ == '__main__':
    main()
