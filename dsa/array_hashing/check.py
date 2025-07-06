from collections import Counter

from certifi import where

# Create a dictionary where values are Counter objects
grouped_counter = {}

# Add Counter objects to the dictionary
grouped_counter[1] = Counter("apple")
grouped_counter[2] = Counter("banana")
grouped_counter[3] = Counter("cherry")

# The Counter object you want to search for
search_counter = Counter("banana")

# # Find the key(s) corresponding to the Counter object
matching_keys = [key for key, value in grouped_counter.items() if value == search_counter]
print(matching_keys)
#
# # Print the result
# if matching_keys:
#     print(f"Matching key(s) for {search_counter}: {matching_keys}")
# else:
#     print(f"No match found for {search_counter}.")