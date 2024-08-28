package main

import (
	"sort"
)

func maximumUnits(boxTypes [][]int, truckSize int) int {
	sort.Slice(boxTypes, func(i, j int) bool{
		return boxTypes[i][1] > boxTypes[j][1]
	})

	var res = 0

	for _, v := range boxTypes{
		if truckSize >= v[0]{
			truckSize -= v[0]
			res += v[1] * v[0]
		} else{
			res += v[1]*truckSize
			break
		}
	}

	return res
}