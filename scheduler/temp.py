# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# node1 = TreeNode(-10)
# node2 = TreeNode(9)
# node3 = TreeNode(20)
# node4 = TreeNode(0)
# node5 = TreeNode(0)
# node6 = TreeNode(-15)
# node7 = TreeNode(7)
# node8 = TreeNode(-10)
# node1.left = node2
# node1.right = node3
# node3.left = node6
# node3.right = node7
# ans = -987654321
# def maxPathSum(root) -> int:

#     dfs(root)
#     return ans

# def dfs(root):
#     if not root:
#         return 0
#     global ans
#     le = dfs(root.left)
#     ri = dfs(root.right) 
#     ans = max(ans, root.val + max(0,le,ri,le+ri))
#     return root.val + max(le, ri, 0)

# print(maxPathSum(root=node1))
import bot

bot.bot_schedule(20)