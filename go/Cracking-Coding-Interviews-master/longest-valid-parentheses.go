package main

import "math"

type stack []int

func (s stack) Push(v int) stack {
	return append(s, v)
}

func (s stack) Pop() (stack, int) {
	l := len(s)
	return s[:l-1], s[l-1]
}

func (s stack) IsEmpty() bool {
	return len(s) == 0
}

func (s stack) Peek() int {
	l := len(s)
	return s[l-1]
}

func IsBalance(s string) int {
	st := make(stack, 0)

	var max float64
	temp := -1
	for j, v := range s {
		if v == '(' {
			st = st.Push(j)
		} else if v == ')' && st.IsEmpty() {
			//return false
			temp = j
		} else {
			st, _ = st.Pop()

			i := temp

			if !st.IsEmpty() {
				i = st.Peek()
			}

			max = math.Max(max, float64(j-i))

		}
	}
	return int(max)
}

func longestValidParentheses(s string) int {
	return IsBalance(s)
}




/***********************************************/


/*
var max float64
	for i := 0; i < len(s); i++ {
		for j := 2; j < len(s); j += 2 {
			if IsBalance(s[i:j]) {
				max = math.Max(max, float64(j-i))
			}
		}
	}

	return int(max)
*/
