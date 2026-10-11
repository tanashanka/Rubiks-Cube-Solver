##### Test movetable-generating functions #####
from cube import CubieCube
from coordinates import (get_twist, set_twist, get_flip, set_flip, 
                         get_slice_coord, set_slice_coord, get_slice_sorted, set_slice_sorted, 
                         get_corners, set_corners, get_ud_edges, set_ud_edges
)
from moves import twist_table, flip_table, slice_table, corners_table, ud_edges_table, slice_sorted_table
from random import randrange



def test_twist_table_matches_direct_computation(samples=200):
    """
    Test that the corner twist coordinate in twist_table matches that of get_twist
    """
    failures = []
    for _ in range(samples):
        x = randrange(2187)
        move = randrange(18)
        c = CubieCube()
        set_twist(c,x)
        c.apply_move(move)
        expected = get_twist(c)
        actual = twist_table()[x][move]
        if actual != expected:
            failures.append(x, move, expected, actual)
    return failures


def test_flip_table_matches_direct_computation(samples=200):
    """
    Test that the edge flip coordinate in flip_table matches that of get_flip
    """
    failures = []
    for _ in range(samples):
        x = randrange(2048)
        move = randrange(18)
        c = CubieCube()
        set_flip(c,x)
        c.apply_move(move)
        expected = get_flip(c)
        actual = flip_table()[x][move]
        if actual != expected:
            failures.append(x, move, expected, actual)
    return failures


def test_slice_table_matches_direct_computation(samples=200):
    """
    Test that the unsorted slice coordinate in slice_table matches that of get_slice_coord
    """
    failures = []
    for _ in range(samples):
        x = randrange(495)
        move = randrange(18)
        c = CubieCube()
        set_slice_coord(c,x)
        c.apply_move(move)
        expected = get_slice_coord(c)
        actual = slice_table()[x][move]
        if actual != expected:
            failures.append(x, move, expected, actual)
    return failures


def test_corners_table_matches_direct_computation(samples=200):
    """
    Test that the corner permutation coordinate in corners_table matches that of get_corners
    """
    failures = []
    for _ in range(samples):
        x = randrange(40320)
        move = randrange(18)
        c = CubieCube()
        set_corners(c,x)
        c.apply_move(move)
        expected = get_corners(c)
        actual = corners_table()[x][move]
        if actual != expected:
            failures.append(x, move, expected, actual)
    return failures


def test_ud_edges_table_matches_direct_computation(samples=200):
    """
    Test that the ud edge permutation coordinate in ud_edges_table matches that of get_ud_edges
    """
    failures = []
    for _ in range(samples):
        x = randrange(40320)
        move = randrange(18)
        c = CubieCube()
        set_ud_edges(c,x)
        c.apply_move(move)
        expected = get_ud_edges(c)
        actual = ud_edges_table()[x][move]
        if actual != expected:
            failures.append(x, move, expected, actual)
    return failures


def test_slice_sorted_p2_table_matches_direct_computation(samples=200):
    """
    Test that the ud edge permutation coordinate in ud_edges_table matches that of get_ud_edges
    """
    failures = []
    for _ in range(samples):
        x = randrange(24)
        move = randrange(18)
        c = CubieCube()
        set_slice_sorted(c,x)
        c.apply_move(move)
        expected = get_slice_sorted(c)
        actual = slice_sorted_table()[x][move]
        if actual != expected:
            failures.append(x, move, expected, actual)
    return failures


if __name__ == "__main__":

    print("Test 1: twist table matches direct computation... ")
    failures1 = test_twist_table_matches_direct_computation()
    print(f"{len(failures1)} failures out of 1000")
    if failures1:
        print(f"First failing case: {failures1[0]}")

    print("Test 2: flip table matches direct computation... ")
    failures2 = test_flip_table_matches_direct_computation()
    print(f"{len(failures2)} failures out of 1000")
    if failures2:
        print(f"First failing case: {failures2[0]}")    

    print("Test 3: unsorted slice table matches direct computation... ")
    failures3 = test_slice_table_matches_direct_computation()
    print(f"{len(failures3)} failures out of 1000")
    if failures3:
        print(f"First failing case: {failures3[0]}")    
    
    print("Test 4: corners table matches direct computation... ")
    failures4 = test_corners_table_matches_direct_computation()
    print(f"{len(failures4)} failures out of 1000")
    if failures4:
        print(f"First failing case: {failures4[0]}")    
    
    print("Test 5: ud edges table matches direct computation... ")
    failures5 = test_ud_edges_table_matches_direct_computation()
    print(f"{len(failures5)} failures out of 1000")
    if failures5:
        print(f"First failing case: {failures5[0]}")

    print("Test 6: slice sorted phase 2 table matches direct computation... ")
    failures6 = test_slice_sorted_p2_table_matches_direct_computation()
    print(f"{len(failures6)} failures out of 1000")
    if failures6:
        print(f"First failing case: {failures6[0]}")
