import hashlib
from functools import reduce
from enum import Enum
from collections import namedtuple

class Dir(Enum):
    left = 1,
    right = 2
    
Step = namedtuple('Step', ['dir', 'hash'])
Path = namedtuple('Path', ['steps', 'leaf_hash'])

class _Node(object):
    def __init__(self, data, dir, left_leaf=None, right_leaf=None):
        self.data = data
        self.dir = dir
        self.parent = None
        self.neighbor = None


class MerkleTree(object):
    def __init__(self, values=[]):
        self.root_hash = None
        self.leaves = []

        #append one more element to make tree even
        if len(values) % 2 == 1:
            values.append(values[-1])

        #create list of leaves which will be used for getting a path
        for i, value in enumerate(values):
            if i % 2 == 0:
                self.__append_left(self.leaves, _Node(sha(value), Dir.right))
            else:
                self.__append_right(self.leaves, _Node(sha(value), Dir.left))

        #iterate over every level of the tree
        past_leaves = list(self.leaves)
        while len(past_leaves) > 1:
            cur_nodes = []
            #walk 2 steps over previous number of elements, reducing by 2 on every level	
            for i, past_i in enumerate(range(0, len(past_leaves), 2)):
                left_leaf = past_leaves[past_i]
                right_leaf = past_leaves[past_i + 1]
                sha_hash = sha(left_leaf.data, right_leaf.data)
                node = None
                if i % 2 == 0:
                    node = _Node(sha_hash, Dir.right)
                    self.__append_left(cur_nodes, node)
                else:
                    node = _Node(sha_hash, Dir.left)
                    self.__append_right(cur_nodes, node)
                left_leaf.parent = node
                right_leaf.parent = node

            # appending new node if number of nodes is odd
            if len(cur_nodes) != 1 and len(cur_nodes) % 2 == 1:
                last_node = cur_nodes[-1]
                self.__append_right(cur_nodes, _Node(last_node.data, Dir.left))

            # we concluded our hashes into final root_hash
            if len(cur_nodes) == 1:
                self.root_hash = cur_nodes[0].data

            past_leaves = list(cur_nodes)         

    def get_path(self, item):
        item_hash = sha(item)
        for leaf in self.leaves:
            if leaf.data == item_hash:
                cur_node = leaf
                steps = []

                while cur_node.parent is not None:
                    neighbor = cur_node.neighbor
                    steps.append(Step(neighbor.dir, neighbor.data))
                    cur_node = cur_node.parent
                if len(steps) > 0:
                    return Path(steps, item_hash)

    @staticmethod
    def verify_path(root_hash, path):
        return MerkleTree.get_root_hash(path) == root_hash
        
    @staticmethod
    def get_root_hash(path):
        branch_hash = path.leaf_hash
        for step in path.steps:
            branch_hash = sha(branch_hash, step.hash) if (step.dir is Dir.left) else sha(step.hash, branch_hash)
        return branch_hash
    
    @staticmethod
    def __append_left(node_list, node):
        node_list.append(node)
    
    @staticmethod
    def __append_right(node_list, node):
        neighbor = node_list[len(node_list) - 1]
        node.neighbor = neighbor
        node_list.append(node)
        neighbor.neighbor = node

def sha(*values):
    return hashlib.sha3_256(reduce(lambda v1, v2: v1 + v2, values).encode('utf-8')).hexdigest()
