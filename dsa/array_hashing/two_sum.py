# https://neetcode.io/problems/two-integer-sum?list=neetcode150
from typing import List


class TwoSum:
    def two_sum_index(self, nums: List[int], target: int) -> List[int]:
        iterate_dict = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in iterate_dict:
                return [iterate_dict[complement], i]
            iterate_dict[num] = i
        return []