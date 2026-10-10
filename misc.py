##### Miscellaneous functions for coordinate calculations #####
from math import comb


def c_nk(n, k):
    """
    Binomial coefficient (n choose k)
    """
    if n < k:
        return 0 # Cannot choose more items than exist
    if k > n // 2: # C(n,k) = C(n,n-k); if k is more than half of n, this line swaps it for the smaller equivalent (n-k); not strictly necessary
        k = n - k
    # C(n,k) = 
    # [n*(n-1)*(n-2)* ... *(n-k+1)]
    # _____________________________
    # [1 * 2 *   3   * ... *  k   ]
    s = 1 # Running result
    i = n # Counts down from n; numerator
    j = 1 # Counts up from 1; denominator
    # Computes one factor at a time (n/1 then [(n-1)/2], etc)
    while i != (n - k): # Runs loop k times; equivalent to for _ in range(k)
        s *= i # Multiplies the next factor of of the numerator into s
        s //= j # Divides the next factor of the denominator into s
        i -= 1 # Decrements numerator by 1
        j += 1 # Increments denominator by 1
    return s

"""
Alternate c_nk using math.comb (already done c_nk function)

    if n < k:
        return 0
    return comb(n, k)
"""


def rotate_arr_left(arr, left, right):
    """
    Rotate the contents of an array bounded by indexes 'left' and 'right' left; includes right
    """
    bound = arr[left]
    for i in range(left, right): # Rotates everything inside the bounds from 'left' to 'right-1' left by reassigning every index to the one after it
        arr[i] = arr[i+1]
    arr[right] = bound # Assigns previous left bound to be current right bound
        


def rotate_arr_right(arr, left, right):
    """
    Rotate the contents of an array bounded by indexes 'left' and 'right' right; includes right
    """
    bound = arr[right]
    for i in range(right, left, -1): # Rotates everything inside the bounds from 'right' to 'left+1' right by reassigning every index to the one before it
        arr[i] = arr[i-1]
    arr[left] = bound # Assigns previous right bound to be current left bound