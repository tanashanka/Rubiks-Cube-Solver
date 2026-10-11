##### Miscellaneous functions for coordinate calculations #####

def c_nk(n, k):
    """
    Binomial coefficient (n choose k)
    """
    if n < k:
        return 0
    if k > n // 2: # Swaps for smaller equivalent
        k = n - k
    # C(n,k) = 
    # [n*(n-1)*(n-2)* ... *(n-k+1)]
    # _____________________________
    # [1 * 2 *   3   * ... *  k   ]
    s = 1 # Running result
    i = n # Counts down from n; numerator
    j = 1 # Counts up from 1; denominator
    # Computes one factor at a time (n/1 then [(n-1)/2], etc)
    while i != (n - k):
        s *= i # Multiplies the next factor of of the numerator into s
        s //= j # Divides the next factor of the denominator into s
        i -= 1
        j += 1
    return s


def rotate_arr_left(arr, left, right):
    """
    Rotate the contents of an array bounded by indexes 'left' and 'right' left; includes right
    """
    bound = arr[left]
    for i in range(left, right):
        arr[i] = arr[i+1] # Rotates everything inside the bounds from 'left' to 'right-1' left by reassigning every index to the one after it
    arr[right] = bound # Assigns previous left bound to be current right bound
        


def rotate_arr_right(arr, left, right):
    """
    Rotate the contents of an array bounded by indexes 'left' and 'right' right; includes right
    """
    bound = arr[right]
    for i in range(right, left, -1):
        arr[i] = arr[i-1]
    arr[left] = bound