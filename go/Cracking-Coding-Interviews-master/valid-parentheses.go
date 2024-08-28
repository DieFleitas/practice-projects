package main

func isValid(s string) bool {
	hm := map[byte]byte{
		'(': ')',
		'{': '}',
		'[': ']',
	}

	stack := make([]byte, 0, len(s))

	for pos := range s {
		c := s[pos]

		if _, ok := hm[c]; ok {
			stack = append(stack, c)
		} else if len(stack) != 0 {
			return false
		} else {
			last := len(stack) - 1
			e := stack[last]
			stack = stack[:last]

			if c != hm[e] {
				return false
			}
		}
	}

	return len(stack) == 0
}
