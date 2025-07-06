import pytest
from dsa.array_hashing.two_sum import TwoSum  # Assuming the function is implemented in two_sum.py

class TestTwoSum:
    def setup_method(self):
        """Setup method to initialize the TwoSum class instance."""
        self.two_sum = TwoSum()

    @pytest.mark.parametrize(
        "nums, target, expected",
        [
            ([2, 7, 11, 15], 9, [0, 1]),  # Example from the problem description
            ([3, 2, 4], 6, [1, 2]),       # Another valid case
            ([3, 3], 6, [0, 1]),          # Two identical numbers
            ([1, 2, 3, 4], 7, [2, 3]),    # Numbers at the end
            ([1, 5, 7, 8], 12, [1, 2]),   # Numbers in the middle
            ([1, 5, 7, 8], 15, [2, 3]),       # No solution
            ([], 5, []),                  # Empty list
            ([1], 2, []),                 # Single element
            ([5, 5, 5, 5], 10, [0, 1]),   # Multiple identical numbers
        ],
    )
    def test_two_sum(self, nums, target, expected):
        """
        Test the two_sum function with various inputs.
        """
        assert self.two_sum.two_sum_index(nums, target) == expected