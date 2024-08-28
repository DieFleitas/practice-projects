package main

import "strings"

func wordPattern(pattern string, str string) bool {
	strs := strings.Split(str, " ")
	patterns := strings.Split(pattern, "")

	if len(pattern) != len(strs) {
		return false
	}

	return checkPattern(patterns, strs) && checkPattern(strs, patterns)
}

func checkPattern(a, b []string) bool {
	dic := make(map[string]string)
	p := 0

	for p < len(a) {
		val, ok := dic[a[p]]
		if !ok {
			dic[a[p]] = b[p]
		} else {
			if val != b[p] {
				return false
			}
		}
		p++
	}

	return true
}
