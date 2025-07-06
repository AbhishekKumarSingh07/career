# https://neetcode.io/problems/duplicate-integer?list=neetcode150
from typing import List


class ContainsDuplicate:
    def has_duplicates(self, nums: List[int]) -> bool:
        check_set = set()
        for num in nums:
            if num in check_set:
                return True
            check_set.add(num)
        return False


