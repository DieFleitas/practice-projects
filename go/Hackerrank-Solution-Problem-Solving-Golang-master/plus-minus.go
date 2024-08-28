package main

import "fmt"

func plusMinus(arr []int32) {
	counts := []int32{0,0,0}

	for _, val := range arr {
		if val > 0 {
			counts[0] += 1
		} else if val < 0 {
			counts[1] += 1
		} else {
			counts[2] += 1
		}
	}

	for _, val := range counts {
		fmt.Printf("%.6f\n", float32(val) / float32(len(arr)))
	}
}