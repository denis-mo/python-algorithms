import unittest
from merkletree import *

class TestMerkleTree(unittest.TestCase):

    def test_verify(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8"])
        path = Path([Step(Dir.right, sha("node1")),
                         Step(Dir.left, sha(sha("node3"), sha("node4"))),
                         Step(Dir.left, sha(sha(sha("node5"), sha("node6")), sha(sha("node7"), sha("node8"))))], 
                        sha("node2"))
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, path), 
                        "MerkleTree.verify falsely don't approve correct branch")
        
    def test_verify_odd_tree(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5"])
        path = Path([Step(Dir.right, sha("node1")),
                         Step(Dir.left, sha(sha("node3"), sha("node4"))),
                         Step(Dir.left, sha(sha(sha("node5"), sha("node5")), sha(sha("node5"), sha("node5"))))], 
                        sha("node2"))
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, path), 
                        "MerkleTree.verify falsely don't approve correct branch for odd tree")
        
    def test_verify_odd_element(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5"])
        path = Path([Step(Dir.left, sha("node5")),
                         Step(Dir.right, sha(sha("node5"), sha("node5"))),
                         Step(Dir.right, sha(sha(sha("node1"), sha("node2")), sha(sha("node3"), sha("node4"))))], 
                        sha("node5"))
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, path), 
                        "MerkleTree.verify falsely don't approve correct branch for odd tree for last element")

    def test_get_path(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8"])
        path = mt.get_path("node5")

        self.assertTrue(MerkleTree.verify_path(mt.root_hash, path), "MerkleTree.get_path returns incorrect path for even tree")
        
    def test_get_path_no_element(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4"])

        self.assertIsNone(mt.get_path("node5"), "MerkleTree.get_path returns incorrect path for even tree")
        
    def test_get_path_odd_tree(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5"])
        branch = mt.get_path("node3")
        
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, branch), "MerkleTree.get_path returns incorrect path for odd tree") 
        
    def test_get_path_odd_element(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5"])
        branch = mt.get_path("node5")
        
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, branch), 
                        "MerkleTree.get_path returns incorrect path for odd tree for the last element")
        
    def test_get_path_big_odd_tree(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7", 
                         "node8", "node9", "node10", "node11", "node12", "node13"])

        self.assertTrue(MerkleTree.verify_path(mt.root_hash, mt.get_path("node1")), 
                        "MerkleTree.get_path or MerkleTree.verify works incorrectly for the first element")
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, mt.get_path("node9")),
                        "MerkleTree.get_path or MerkleTree.verify works incorrectly for the element in the middle")
        self.assertTrue(MerkleTree.verify_path(mt.root_hash, mt.get_path("node13")), 
                        "MerkleTree.get_path or MerkleTree.verify works incorrectly for the last element")
        
    def test_get_path_fake_tree(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8"])
        path = mt.get_path("node5")
        fake_mt = MerkleTree(["node1", "node2", "node3", "node4", "fake_node", "node6", "node7", "node8"])
        fake_path = fake_mt.get_path("fake_node")

        self.assertFalse(MerkleTree.verify_path(mt.root_hash, fake_path),
                         "Merkle tree with counterfeit node incorrectly verified")

if __name__ == '__main__':
    unittest.main()
