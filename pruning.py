##### Pruning tables reduce the size of the search tree during the search
from cube import CubieCube, Cor, Edg
from coordinates import get_twist, set_twist, get_flip, set_flip, get_slice_coord, set_slice_coord, get_corners, set_corners, get_ud_edges, set_ud_edges, get_slice_sorted, set_slice_sorted
from constants import N_TWIST, N_FLIP, N_SLICE, N_SLICE_SORTED, N_SLICE_SORTED_P2, N_CORNERS, N_UD_EDGES, N_MOVES, PHASE_2_MOVES
from moves import twist_table, flip_table, slice_table, corners_table, ud_edges_table, slice_sorted_table
from collections import deque


##### Phase 1 pruning tables #####
def pack_twist(twist_coord, slice_coord):
    """
    Pack twist and unsorted slice into a coordinate from 0-1082564 (N_TWIST * N_SLICE -1) to represent each (twist,slice) pair
    """
    return twist_coord * N_SLICE + slice_coord


def build_twist_slice_table(twist_table, slice_table):
    """
    Build a combined lookup table from twist_table and slice_table
    """
    size = N_TWIST * N_SLICE # Total number of states/entries
    dist = [-1] * size # One slot per state, starting at an unused number; describes shortest distance from that state to solved

    start = pack_twist(0,0) # Start table from solved coord (0,0)
    dist[start] = 0 # Distance from solved to solved = 0

    queue = deque([start]) # Start queue with starting state
    while queue: # Keep processing for every state in queue
        current = queue.popleft() # Current state is the next unprocessed one
        current_dist = dist[current]

        twist_coord, slice_coord = divmod(current, N_SLICE) # Split current into twist and slice_coord

        for m in range(N_MOVES): # Try every move from current state
            new_twist = twist_table[twist_coord][m]
            new_slice = slice_table[slice_coord][m]
            subsequent = pack_twist(new_twist, new_slice) # Repack new coords into a combined index to be stored in dist

            if dist[subsequent] == -1:
                dist[subsequent] = current_dist + 1
                queue.append(subsequent)

    return dist


def pack_flip(flip_coord, slice_coord):
    """
    Pack flip and unsorted slice into a coordinate from 0-1013759 (N_FLIP * N_SLICE -1) to represent each (flip,slice) pair
    """
    return flip_coord * N_SLICE + slice_coord


def build_flip_slice_table(flip_table, slice_table):
    """
    Build a combined lookup table from flip_table and slice_table
    """
    size = N_FLIP * N_SLICE
    dist = [-1] * size

    start = pack_flip(0,0)
    dist[start] = 0

    queue = deque([start])
    while queue:
        current = queue.popleft()
        current_dist = dist[current]

        flip_coord, slice_coord = divmod(current, N_SLICE)

        for m in range(N_MOVES):
            new_flip = flip_table[flip_coord][m]
            new_slice = slice_table[slice_coord][m]
            subsequent = pack_flip(new_flip, new_slice)

            if dist[subsequent] == -1:
                dist[subsequent] = current_dist + 1
                queue.append(subsequent)

    return dist


##### Phase 2 pruning tables #####
def pack_corners(corners_coord, slice_sorted_p2):
    """
    Pack corners and phase 2 sorted slice into a coordinate from 0-967679 (N_CORNERS * N_SLICE_SORTED_P2 -1) to represent each (corner,slice_sorted_p2) pair
    """
    return corners_coord * N_SLICE_SORTED_P2 + slice_sorted_p2


def build_corners_slice_p2_table(corners_table, slice_table):
    """
    Build a combined lookup table from corners_table and slice_sorted_table
    """
    size = N_CORNERS * N_SLICE_SORTED_P2
    dist = [-1] * size

    start = pack_corners(0,0)
    dist[start] = 0

    queue = deque([start])
    while queue:
        current = queue.popleft()
        current_dist = dist[current]

        corners_coord, slice_coord = divmod(current, N_SLICE_SORTED_P2)

        for m in PHASE_2_MOVES:
            new_corners = corners_table[corners_coord][m]
            new_slice = slice_table[slice_coord][m]
            subsequent = pack_corners(new_corners, new_slice)

            if dist[subsequent] == -1:
                dist[subsequent] = current_dist + 1
                queue.append(subsequent)

    return dist


def pack_ud_edges(ud_edges_coord, slice_sorted_p2):
    """
    Pack UD edges and phase 2 sorted slice into a coordinate from 0-967679 (N_UD_EDGES * N_SLICE_SORTED_P2 -1) to represent each (ud_edge,slice_sorted_p2) pair
    """
    return ud_edges_coord * N_SLICE_SORTED_P2 + slice_sorted_p2


def build_ud_edges_slice_p2_table(ud_edges_table, slice_table):
    """
    Build a combined lookup table from ud_edges_table and slice_sorted_table
    """
    size = N_UD_EDGES * N_SLICE_SORTED_P2
    dist = [-1] * size

    start = pack_ud_edges(0,0)
    dist[start] = 0

    queue = deque([start])
    while queue:
        current = queue.popleft()
        current_dist = dist[current]

        ud_edges_coord, slice_coord = divmod(current, N_SLICE_SORTED_P2)

        for m in PHASE_2_MOVES:
            new_ud_edges = ud_edges_table[ud_edges_coord][m]
            new_slice = slice_table[slice_coord][m]
            subsequent = pack_ud_edges(new_ud_edges, new_slice)

            if dist[subsequent] == -1:
                dist[subsequent] = current_dist + 1
                queue.append(subsequent)

    return dist