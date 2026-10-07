from collections import deque


class TreeNode:

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)


def isSymmetric(root):
    def check(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2 or t1.val != t2.val:
            return False
        return check(t1.left, t2.right) and check(t1.right, t2.left)

    return check(root, root)


def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root


def kthSmallest(root, k):
    stack = []
    curr = root
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right


class Codec:

    def serialize(self, root):
        res = []

        def dfs(node):
            if not node:
                res.append("None")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        vals = deque(data.split(","))

        def dfs():
            val = vals.popleft()
            if val == "None":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


def maxPathSum(root):
    max_sum = float("-inf")

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        max_sum = max(max_sum, node.val + left + right)
        return node.val + max(left, right)

    dfs(root)
    return max_sum


def minCameraCover(root):
    cameras = 0

    def dfs(node):
        nonlocal cameras
        if not node:
            return 1
        left = dfs(node.left)
        right = dfs(node.right)
        if left == 0 or right == 0:
            cameras += 1
            return 2
        if left == 2 or right == 2:
            return 1
        return 0

    if dfs(root) == 0:
        cameras += 1
    return cameras


def verticalTraversal(root):
    from collections import defaultdict

    nodes = defaultdict(list)

    def dfs(node, r, c):
        if not node:
            return
        nodes[c].append((r, node.val))
        dfs(node.left, r + 1, c - 1)
        dfs(node.right, r + 1, c + 1)

    dfs(root, 0, 0)
    res = []
    for c in sorted(nodes.keys()):
        col_nodes = sorted(nodes[c], key=lambda x: (x[0], x[1]))
        res.append([val for r, val in col_nodes])
    return res


def recoverFromPreorder(traversal):
    stack = []
    i = 0
    n = len(traversal)
    while i < n:
        depth = 0
        while i < n and traversal[i] == "-":
            depth += 1
            i += 1
        val = 0
        while i < n and traversal[i].isdigit():
            val = val * 10 + int(traversal[i])
            i += 1
        node = TreeNode(val)
        while len(stack) > depth:
            stack.pop()
        if stack:
            if not stack[-1].left:
                stack[-1].left = node
            else:
                stack[-1].right = node
        stack.append(node)
    return stack[0] if stack else None


if __name__ == "__main__":
    p = TreeNode(1, TreeNode(2), TreeNode(3))
    q = TreeNode(1, TreeNode(2), TreeNode(3))
    print("Task 1:", isSameTree(p, q))

    root2 = TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))
    print("Task 2:", isSymmetric(root2))

    root3 = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
    inverted = invertTree(root3)
    print("Task 3 (Inverted root):", inverted.val)

    root4 = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
    print("Task 4 (1st smallest):", kthSmallest(root4, 1))

    codec = Codec()
    serialized = codec.serialize(root3)
    print("Task 5 (Serialized):", serialized)

    root6 = TreeNode(1, TreeNode(2), TreeNode(3))
    print("Task 6 (Max path sum):", maxPathSum(root6))

    root7 = TreeNode(0, TreeNode(0, TreeNode(0), TreeNode(0)))
    print("Task 7 (Min cameras):", minCameraCover(root7))

    root8 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print("Task 8 (Vertical traversal):", verticalTraversal(root8))

    recovered = recoverFromPreorder("1-2--3--4-5--6--7")
    print("Task 9 (Recovered root):", recovered.val if recovered else None)