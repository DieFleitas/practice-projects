package main

func diagonalDifference(arr [][]int32) int32 {
	sum := []int32{0, 0}

	for i := 0; i < len(arr); i++ {
		sum[0] += arr[i][i]

		opponent := len(arr) - i - 1
		sum[1] += arr[i][opponent]
	}

	return abs(sum[0] - sum[1])
}

func abs(num int32) int32 {
	if num < 0 {
		return num * -1
	}

	return num
}
