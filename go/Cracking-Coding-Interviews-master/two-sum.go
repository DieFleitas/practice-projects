package main

func twoSum(nums []int, target int) []int {
	hm := make(map[int]int)

	for i, v := range nums {
		if j, ok := hm[v]; ok {
			return []int{i, j}
		} else {
			hm[target-v] = i
		}
	}
	return nil
}

/*
for i := 0; i < len(nums); i++ {
		for j:=i+1; j <len(nums); j++ {
			if (nums[i] + nums[j] == target){
				return []int{i, j}
			}
		}
	}
	return nil
*/
