package main

func aVeryBigSum(ar []int64) int64 {
	sum := int64(0)

	for _, val := range ar {
		sum += val
	}

	return sum
}