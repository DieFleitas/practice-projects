package main

func Factorial(n int) int {
	if n < 2 {
		return 1
	}

	return n * Factorial(n-1)
}