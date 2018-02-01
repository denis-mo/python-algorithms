import hashlib
from functools import reduce


class Node(object):
    def __init__(self, data, side, neighbor=None, left_leaf=None, right_leaf=None):
        self.data = data
        self.side = side
        self.parent = None
        self.neighbor = neighbor
        if left_leaf is not None:
            left_leaf.parent = self
            right_leaf.parent = self
        if neighbor is not None:
            neighbor.neighbor = self


class MerkleTree(object):
    def __init__(self, values=[]):
        self.root_hash = ""
        self.leaves = []

        if len(values) % 2 == 1:
            values.append(values[-1])

        for past_i, value in enumerate(values):
            if past_i % 2 == 0:
                self.leaves.append(Node(sha(value), 1))
            else:
                self.leaves.append(Node(sha(value), 0, self.leaves[past_i - 1]))

        past_leaves = list(self.leaves)

        while len(past_leaves) > 1:
            current_nodes = []
            for i, past_i in enumerate(range(0, len(past_leaves), 2)):
                left_leaf = past_leaves[past_i]
                right_leaf = past_leaves[past_i + 1]
                sha_hash = sha(left_leaf.data, right_leaf.data)
                if i % 2 == 0:
                    node = Node(sha_hash, 1, None, left_leaf, right_leaf)
                else:
                    node = Node(sha_hash, 0, current_nodes[i - 1], left_leaf, right_leaf)
                current_nodes.append(node)

            # appending new node if number of nodes is even
            if len(current_nodes) != 1 and len(current_nodes) % 2 == 1:
                last_node = current_nodes[-1]
                current_nodes.append(Node(last_node.data, 0, last_node))

            if len(current_nodes) == 1:
                self.root_hash = current_nodes[0].data

            past_leaves = list(current_nodes)

    def validate(self, item="", path=[]):
        path = list(path)
        path.insert(0, sha(item))
        root_hash = reduce(self.merklestep, path)
        return True if root_hash == self.root_hash else False

    def get_path(self, item):
        sha_hash = sha(item)
        for i, leaf in enumerate(self.leaves):
            if leaf.data == sha_hash:
                current_node = leaf
                path = []

                while current_node.parent is not None:
                    neighbor = current_node.neighbor
                    path.append((neighbor.side, neighbor.data))
                    current_node = current_node.parent
                if len(path) > 0:
                    return path

    @staticmethod
    def merklestep(prev_hash, side):
        if side[0] is 0:
            return sha(prev_hash, side[1])
        else:
            return sha(side[1], prev_hash)


def sha(val1, val2=None):
    if val2 is None:
        return hashlib.sha3_256(val1.encode('utf-8')).hexdigest()
    return hashlib.sha3_256(val1.encode('utf-8') + val2.encode('utf-8')).hexdigest()