# Functions for searching and subsetting a sorted list of objects
#
# This code is partially modified from the 'bisect' module, which only works on a sorted list of values.
# These functions deal with array of objects that are sorted by field.

# Returns index of smallest item in 'array' whose 'key' is larger than or equal to 'value'
# Returns len(array) if there is no such object
def bisect_left(array, value, key):
    lo = 0
    hi = len(array)
    while lo < hi:
        mid = (lo+hi)//2
        if array[mid][key] < value: lo = mid+1
        else: hi = mid
    return lo

# Returns index of largets item in 'array' whose 'key' is smaller than or equal to 'value'
# Returns 0 if there is no such object.
def bisect_right(array, value, key):
    lo = 0
    hi = len(array)
    while lo < hi:
        mid = (lo+hi)//2
        if value < array[mid][key]: hi = mid
        else: lo = mid+1
    return lo

# For a sorted array, returns a slice of objects o such that min <= o[key] <= max
def get_subinterval(array, min, max, key):
    smallest = bisect_left(array, min, key)
    if smallest == len(array):
        return []

    largest = bisect_right(array, max, key)
    if not largest:
        return []

    return array[smallest:largest]
