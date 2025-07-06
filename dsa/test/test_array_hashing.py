import pytest
from dsa.array_hashing.contains_duplicate import ContainsDuplicate


class TestContainsDuplicate:
    def setup_method(self):
        """Setup method to initialize the ContainsDuplicate class instance."""
        self.contains_duplicate = ContainsDuplicate()

    @pytest.mark.parametrize(
        "nums, expected",
        [
            ([1, 2, 3, 4], False),  # No duplicates
            ([1, 2, 3, 1], True),   # Contains duplicates
            ([], False),            # Empty list
            ([1], False),           # Single element
            ([1, 1, 1, 1], True),   # All duplicates
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False),  # Large list, no duplicates
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 1], True),    # Large list, with duplicates
        ],
    )
    def test_has_duplicates(self, nums, expected):
        """Test the has_duplicates method with various inputs."""
        assert self.contains_duplicate.has_duplicates(nums) == expected

    def test_invalid_input(self):
        """Test the has_duplicates method with invalid input."""
        with pytest.raises(TypeError):
            self.contains_duplicate.has_duplicates(None)  # Passing None should raise TypeError