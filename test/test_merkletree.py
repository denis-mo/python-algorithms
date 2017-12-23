import unittest
from merkletree.merkletree import MerkleTree, sha


class TestMerkleTree(unittest.TestCase):

    def test_validate(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8"])
        path = [(1, sha("node1")),
                (0, sha(sha("node3"), sha("node4"))),
                (0, sha(sha(sha("node5"), sha("node6")), sha(sha("node7"), sha("node8"))))]

        self.assertTrue(mt.validate("node2", path))

    def test_get_path(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8"])
        path = mt.get_path("node5")

        self.assertFalse(mt.validate("node2", path))
        self.assertTrue(mt.validate("node5", path))

    def test_get_path_odd(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5", "node6", "node7"])
        path = mt.get_path("node7")

        self.assertFalse(mt.validate("node3", path))
        self.assertTrue(mt.validate("node7", path))

    def test_get_path_odd_path(self):
        mt = MerkleTree(["node1", "node2", "node3", "node4", "node5"])
        path = mt.get_path("node5")

        self.assertFalse(mt.validate("node3", path))
        self.assertTrue(mt.validate("node5", path))


if __name__ == '__main__':
    unittest.main()
