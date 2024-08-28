package main

func maxArea(height []int) int {

	i := 0
	j := len(height) - 1
	max := 0

	for i < j {
		area := min(height[i], height[j]) * (j - i)

		if area > max {
			max = area
		} else if height[i] < height[j] {
			i++
		} else {
			j--
		}
	}
	return max
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
