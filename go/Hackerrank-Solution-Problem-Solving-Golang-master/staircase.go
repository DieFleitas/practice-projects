package main

import "fmt"

func staircase(n int32) {
	for i := int32(0); i < n; i++ {
		row := ""

		for j := int32(0); j < n-i-1; j++ {
			row = fmt.Sprintf("%s ", row)
		}

		for j := int32(0); j <= i; j++ {
			row = fmt.Sprintf("%s#", row)
		}

		fmt.Println(row)
	}
}
