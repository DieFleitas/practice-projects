package main 

/* definition for singly-linked list*/
type ListNode struct {
	Val int
	Next *ListNode
}

func mergeTwoLists(list1 *ListNode, list2 *ListNode) *ListNode {

	a := list1
	b := list2

	head := ListNode{}
	curr := &head

	for a !=nil && b != nil {
		if a.Val < b.Val {
			curr.Next = a
			a = a.Next
		} else {
			curr.Next = b
			b = b.Next
		}

		curr = curr.Next
	}

	if a != nil {
		curr.Next = a
	}

	if b!= nil {
		curr.Next = b
	}

	return head.Next
}