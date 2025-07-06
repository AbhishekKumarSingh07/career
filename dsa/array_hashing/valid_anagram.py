#https://neetcode.io/problems/is-anagram?list=neetcode150
from collections import Counter


class ValidAnagram:
    def is_anagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)



