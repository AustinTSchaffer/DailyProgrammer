# Construct Binary Tree from Inorder and Postorder Traversal

https://leetcode.com/explore/challenge/card/july-leetcoding-challenge/547/week-4-july-22nd-july-28th/3403/

Given inorder and postorder traversal of a tree, construct the binary tree.

# Example

```
inorder = [9,3,15,20,7]
postorder = [9,15,7,20,3]
```

Return the following binary tree:

```
    3
   / \
  9  20
    /  \
   15   7
```

## Notes

You may assume that duplicates do not exist in the tree.


## Thought Process

From https://en.wikipedia.org/wiki/Tree_traversal#In-order_(LNR)

> **In-order (LNR)**
> 
> 1. Traverse the left subtree by recursively calling the in-order function.
> 2. Access the data part of the current node.
> 3. Traverse the right subtree by recursively calling the in-order function.
> 
> **Post-order (LRN)**
> 
> 1. Traverse the left subtree by recursively calling the post-order function.
> 2. Traverse the right subtree by recursively calling the post-order function.
> 3. Access the data part of the current node.

In both preorder and postorder, the left-most node will be first. In postorder,
the root node will be last. This entire problem will be solved by correlating
information between these 2 lists.

- Create a recursive function within the entrypoint function, accepting the 2
  order lists and a pointer to a TreeNode object that allows the inner function
  to add to the tree.
- Pop the last value from postorder. Set the current node's value to its value.
- Find the value within preorder. Split preorder into halves around that value.
- Split postorder into halves based on the lengths of the halves of preorder.
- If any in the left half of preorder, create a treenode, set it as "left" on
  the current node. Recurse using the left halves of preorder/postorder.
- If any in the right half of preorder, create a treenode, set it as "right" on
  the current node. Recurse using the right halves of preorder/postorder.
