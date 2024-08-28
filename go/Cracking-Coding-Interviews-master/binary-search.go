package main

func search(nums []int, target int) int {
	return search2(nums, target, 0, len(nums)-1)
}

func search2(nums []int, target int, lo int, hi int) int {

	if lo > hi {
		return -1
	}

	m := lo + (hi+lo)/2

	if nums[m] < target {
		return search2(nums, target, m+1, hi)
	}
	if nums[m] > target {
		return search2(nums, target, lo, m-1)
	}

	return m
}

/************************************************************/

/*
hi := len(nums) -1
	lo := 0

	for lo <= hi {
		m := lo + (hi + lo) / 2

		if nums[m] == target{
			return m
		} else if nums[m] < target{
			lo = m +1
		} else {
			hi = m -1
		}
	}

	return -1


*/

/************************************************************/

/*
i := sort.SearchInts(nums, target)

	if i < len(nums) && nums[i] == target {
		return i
	}

	return -1

*/
