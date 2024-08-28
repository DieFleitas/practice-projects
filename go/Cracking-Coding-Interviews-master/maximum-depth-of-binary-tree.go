package main

/**
* definition for a binary tree node*/
type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func Max(a, b int) int {
	if a > b {
		return a
	}

	return b
}

func maxDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}

	return 1 + Max(maxDepth(root.Left), maxDepth(root.Right))
}
