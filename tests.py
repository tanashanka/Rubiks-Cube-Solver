##### Collection of tests #####
from cube import CubieCube, moveCube
from constants import Move
from scramble import scramble
from coordinates import get_twist, set_twist, get_flip, set_flip, get_slice_coord, set_slice_coord, get_slice_sorted, set_slice_sorted, get_corners, set_corners, get_ud_edges, set_ud_edges
from moves import twist_table, flip_table, slice_table, corners_table, ud_edges_table, slice_sorted_table
from random import randrange


# Applying the same move 4 times should return the cube to solved
def test_four_moves_to_solved(trials=1000):
    failures = []
    for trial in range(trials):
        c = CubieCube()
        i = randrange(Move.U1,Move.B3)
        c.apply_move(i) 
        c.apply_move(i)
        c.apply_move(i)
        c.apply_move(i)
        if not c.is_solved():
            failures.append((trial))
    return failures


def inv_move(m):
    """
    Find the inverse of a given move m
    """
    col, k = divmod(m, 3) # Divides m by 3, puts quotient into col, remainder into k
    return 3 * col + (2 - k) # Inverse of moveCube formula


# Inverse scramble moves test
def test_reverse_moves(trials=1000, moves=25):
    """
    Do inverse moves in reverse order of the scramble
    """
    failures = []
    for trial in range(trials):
        c = CubieCube()
        move_list = scramble(c, moves) # List of 25-move scramble
        for m in reversed(move_list): # Reverses the moves generated from scramble()
            c.apply_move(inv_move(m))
        if not c.is_solved():
            failures.append((trial,move_list))
    return failures


# Inverse scramble state test
def test_inv_cube_state(trials=1000, moves=25):
    """
    Reverses the moves done by a given scramble to return a cube to solved
    """
    failures = []
    for trial in range(trials):
        c = CubieCube()
        move_list = scramble(c, moves) # List of 25-move scramble
        d = CubieCube()
        c.inverse_cubie_cube(d) # Computes inverse of cubiecube
        c.multiply(d) # Multiplies cubiecube with its inverse
        if not c.is_solved():
            failures.append((trial,move_list))
    return failures


# get_/set_twist roundtrip test
def test_twist_roundtrip(trials=1000, moves=25):
    """
    Checks that recomputing the coordinate integer via set_twist returns the same value as computing the integer through get_twist and an original scramble
    """
    failures = []
    for trial in range(trials):
        c = CubieCube()
        scramble(c, moves)
        original = get_twist(c)

        d = CubieCube()
        set_twist(d, original)
        recomputed = get_twist(d)

        if original != recomputed:
            failures.append((trial, original, recomputed))
    return failures


# set_twist to get_twist for every coord
def test_twist_exhaustive():
    """
    Tests the set_twist -> get_twist direction for every coordinate value
    """
    failures = []
    for i in range(2187):
        c = CubieCube()
        set_twist(c, i)
        if get_twist(c) != i:
            failures.append(i)
    return failures



# get_/set_flip roundtrip test
def test_flip_roundtrip(trials=1000, moves=25):
    """
    Checks that recomputing the coordinate integer via set_flip returns the same value as computing the integer through get_flip and an original scramble
    """
    failures = []
    for trial in range(trials):
        c = CubieCube()
        scramble(c, moves)
        original = get_flip(c)

        d = CubieCube()
        set_flip(d, original)
        recomputed = get_flip(d)

        if original != recomputed:
            failures.append((trial, original, recomputed))
    return failures


# set_flip to get_flip for every coord
def test_flip_exhaustive():
    """
    Tests the set_flip -> get_flip direction for every coordinate value
    """
    failures = []
    for i in range(2048):
        c = CubieCube()
        set_flip(c, i)
        if get_flip(c) != i:
            failures.append(i)
    return failures


# get_/get_slice_coord roundtrip test
def test_slice_roundtrip(trials=1000, moves=25):
    """
    Tests that recomputing unsorted slice coord via set_slice_coord returns the same value as computing the integer through get_slice_coord and an original scramble
    """
    failures = []
    for trial in range(trials):
        c = CubieCube()
        scramble(c, moves)
        original = get_slice_coord(c)

        d = CubieCube()
        set_slice_coord(d, original)
        recomputed = get_slice_coord(d)

        if original != recomputed:
            failures.append((trial, original, recomputed))
    return failures


# get_/set_slice_sorted roundtrip test
def test_slice_sorted_roundtrip_exhaustive():
    """
    Tests that recomputing sorted slice coord via set_slice_sorted returns the same value as computing the integer through get_slice_sorted for all coordinate values
    """
    failures = []
    for coord in range(11880):
        c = CubieCube()
        set_slice_sorted(c, coord)
        result = get_slice_sorted(c)
        if result != coord:
            failures.append((coord, result))
    return failures


def test_corners_roundtrip_exhaustive():
    """
    Test that recomputing corner permutation coord via set_corners returns the same value as computing the integer through get_corners for all coordinate values
    """
    failures = []
    for coord in range(40320):
        c = CubieCube()
        set_corners(c, coord)
        result = get_corners(c)
        if result != coord:
            failures.append((coord, result))
    return failures


def test_ud_edges_roundtrip_exhaustive():
    """
    Test that recomputing the edge permutation coord via set_ud_edges returns the same value as computing the integer through get_ud_edges for all coordinate values
    """
    failures = []
    for coord in range(40320):
        c = CubieCube()
        set_ud_edges(c, coord)
        result = get_ud_edges(c)
        if result != coord:
            failures.append((coord, result))
    return failures


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



if __name__ == "__main__":
    print("Test 1: four moves return to solved test...")
    failures1 = test_four_moves_to_solved()
    print(f"{len(failures1)} failures our of 1000")
    if failures1:
        print(f"First failing case: {failures1[0]}")

    print("Test 2: inverse scramble moves test...")
    failures2 = test_reverse_moves()
    print(f"{len(failures2)} failures out of 1000")
    if failures2:
        print(f"First failing case: {failures2[0]}")

    print("Test 3: inverse scramble state test...")
    failures3 = test_inv_cube_state()
    print(f"{len(failures3)} failures out of 1000")
    if failures3:
        print(f"First failing case: {failures3[0]}")

    print("Test 4: get/set twist roundtrip test... ")
    failures4 = test_twist_roundtrip()
    print(f"{len(failures4)} failures out of 1000")
    if failures4:
        print(f"First failing case: {failures4[0]}")

    print("Test 5: set twist exhaustive test... ")
    failures5 = test_twist_exhaustive()
    print(f"{len(failures5)} failures out of 1000")
    if failures5:
        print(f"First failing case: {failures5[0]}")

    print("Test 6: get/set flip roundtrip test... ")
    failures6 = test_flip_roundtrip()
    print(f"{len(failures6)} failures out of 1000")
    if failures6:
        print(f"First failing case: {failures6[0]}")

    print("Test 7: set flip exhaustive test... ")
    failures7 = test_flip_exhaustive()
    print(f"{len(failures7)} failures out of 1000")
    if failures7:
        print(f"First failing case: {failures7[0]}")

    print("Test 8: get/set slice roundtrip test... ")
    failures8 = test_slice_roundtrip()
    print(f"{len(failures8)} failures out of 1000")
    if failures8:
        print(f"First failing case: {failures8[0]}")

    print("Test 9: get/set slice sorted exhaustive roundtrip test... ")
    failures9 = test_slice_sorted_roundtrip_exhaustive()
    print(f"{len(failures9)} failures out of 1000")
    if failures9:
        print(f"First failing case: {failures9[0]}")

    print("Test 10: get/set corners exhaustive roundtrip test... ")
    failures10 = test_corners_roundtrip_exhaustive()
    print(f"{len(failures10)} failures out of 1000")
    if failures10:
        print(f"First failing case: {failures10[0]}")

    print("Test 11: get/set ud edges exhaustive roundtrip test... ")
    failures11 = test_ud_edges_roundtrip_exhaustive()
    print(f"{len(failures11)} failures out of 1000")
    if failures11:
        print(f"First failing case: {failures11[0]}")

    print("Test 12: twist table matches direct computation... ")
    failures12 = test_twist_table_matches_direct_computation()
    print(f"{len(failures12)} failures out of 1000")
    if failures12:
        print(f"First failing case: {failures12[0]}")

    print("Test 13: flip table matches direct computation... ")
    failures13 = test_flip_table_matches_direct_computation()
    print(f"{len(failures13)} failures out of 1000")
    if failures13:
        print(f"First failing case: {failures13[0]}")    

    print("Test 14: unsorted slice table matches direct computation... ")
    failures14 = test_slice_table_matches_direct_computation()
    print(f"{len(failures14)} failures out of 1000")
    if failures14:
        print(f"First failing case: {failures14[0]}")    