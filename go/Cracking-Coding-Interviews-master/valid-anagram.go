package main

func isAnagram(s, t string) bool {
	hm := make(map[rune]int)

	for _, v := range s {
		hm[v]++
	}

	for _, v := range t {
		hm[v]--

		if hm[v] < 0{
			return false
		}
	}

	return len(s) == len(t)
}