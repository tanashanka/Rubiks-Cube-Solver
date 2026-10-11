##### Generates movetables that describe the transformation of the coordinates by cube moves #####
from cube import CubieCube, Cor, Edg
from coordinates import (get_twist, set_twist, get_flip, set_flip, 
                         get_slice_coord, set_slice_coord, get_corners, set_corners, 
                         get_ud_edges, set_ud_edges, get_slice_sorted, set_slice_sorted
)
from constants import (N_TWIST, N_FLIP, N_SLICE, N_SLICE_SORTED_P2, 
                       N_CORNERS, N_UD_EDGES, N_MOVES, PHASE_2_MOVES
)


##### Phase 1 movetables #####
def twist_table():
    """
    Build a lookup table that tells the new twist coordinate for a given twist coordinate and move applied
    """
    table = [[0] * 18 for _ in range(N_TWIST)] # Generate an empty table where for all coordinates in N_TWIST, you can find a new coordinate for a given move applied
    for i in range(N_TWIST):
        c = CubieCube()
        set_twist(c,i) # Encode the corner orientation for each coordinate i into c.co
        for m in range(N_MOVES):
            d = CubieCube(c.cp, c.co, c.ep, c.eo)
            d.apply_move(m) # Try each move on d
            table[i][m] = get_twist(d) # Reads resulting twist coord from d, stores it in table at (i,m)
    return table


def flip_table():
    """
    Build a lookup table that tells the new flip coordinate for a given flip coordinate and move applied
    """
    table = [[0] * 18 for _ in range(N_FLIP)]
    for i in range(N_FLIP):
        c = CubieCube()
        set_flip(c,i)
        for m in range(N_MOVES):
            d = CubieCube(c.cp, c.co, c.ep, c.eo)
            d.apply_move(m)
            table[i][m] = get_flip(d)
    return table


def slice_table():
    """
    Build a lookup table that tells the new unsorted slice coord for a given slice coord and move applied
    """
    table = [[0] * 18 for _ in range(N_SLICE)]
    for i in range(N_SLICE):
        c = CubieCube()
        set_slice_coord(c,i)
        for m in range(N_MOVES):
            d = CubieCube(c.cp, c.co, c.ep, c.eo)
            d.apply_move(m)
            table[i][m] = get_slice_coord(d)
    return table


##### Phase 2 movetables #####
def corners_table():
    """
    Build a lookup table that tells the new corner permutation coord for a given corner permutation coord and move applied
    """
    table = [[0] * 18 for _ in range(N_CORNERS)]
    for i in range(N_CORNERS):
        c = CubieCube()
        set_corners(c,i)
        for m in range(N_MOVES):
            d = CubieCube(c.cp, c.co, c.ep, c.eo)
            d.apply_move(m)
            table[i][m] = get_corners(d)
    return table


def ud_edges_table():
    """
    Build a lookup table that tells you the new ud edge permutation coord for a given ud edge permutation coord and move applied
    """
    table = [[0] * 18 for _ in range(N_UD_EDGES)]
    for i in range(N_UD_EDGES):
        c = CubieCube()
        set_ud_edges(c,i)
        for m in PHASE_2_MOVES:
            d = CubieCube(c.cp, c.co, c.ep, c.eo)
            d.apply_move(m)
            table[i][m] = get_ud_edges(d)
    return table


def slice_sorted_table():
    """
    Build a lookup table that tell you the new sorted slice edge permutation coord for a given sorted slice edge permutation coord and move applied
    """
    table = [[0] * 18 for _ in range(N_SLICE_SORTED_P2)]
    for i in range(N_SLICE_SORTED_P2):
        c = CubieCube()
        set_slice_sorted(c,i)
        for m in range(N_MOVES):
            d = CubieCube(c.cp, c.co, c.ep, c.eo)
            d.apply_move(m)
            table[i][m] = get_slice_sorted(d)
    return table