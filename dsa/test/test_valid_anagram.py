import pytest
from dsa.array_hashing.valid_anagram import ValidAnagram  # Assuming the class is in valid_anagram.py

class TestValidAnagram:
    def setup_method(self):
        """Setup method to initialize the ValidAnagram class instance."""
        self.valid_anagram = ValidAnagram()

    @pytest.mark.parametrize(
        "s, t, expected",
        [
            ("anagram", "nagaram", True),  # Valid anagram
            ("rat", "car", False),        # Not an anagram
            ("", "", True),               # Both strings are empty
            ("a", "a", True),             # Single character, same
            ("a", "b", False),            # Single character, different
            ("abc", "cba", True),         # Valid anagram
            ("abc", "abcd", False),       # Different lengths
            ("listen", "silent", True),   # Valid anagram
            ("hello", "oellh", True),     # Valid anagram
            ("hello", "world", False),    # Not an anagram
        ],
    )
    def test_is_anagram(self, s, t, expected):
        """Test the is_anagram method with various inputs."""
        assert self.valid_anagram.is_anagram(s, t) == expected

    def test_invalid_input(self):
        """Test the is_anagram method with invalid input."""
        with pytest.raises(TypeError):
            self.valid_anagram.is_anagram(None, "test")  # Invalid input
        with pytest.raises(TypeError):
            self.valid_anagram.is_anagram("test", None)  # Invalid input
        with pytest.raises(TypeError):
            self.valid_anagram.is_anagram(123, 456)      # Non-string input