##### Implements the solving algorithm #####
import time
from cube import CubieCube
from constants import N_MOVES, PHASE_2_MOVES
from coordinates import get_twist, get_flip, get_slice_coord, get_slice_sorted, get_corners, get_ud_edges
from pruning import pack_twist, pack_flip, pack_corners, pack_ud_edges


##### Phase 1 search/solve #####
def phase1_search(twist, flip, slice_coord, path, threshold, last_face, tables):
    """
    Recursive IDA* search for a Phase 1 solution within a given movecount threshold
    
    twist, flip, slice_coord = current search node's coords
    path = moves taken so far
    threshold = movecount ceiling for this iteration
    last_face = face of previous move
    tables = Tables namedtuple from build_all_tables

    Returns move list if a solution is found at/under threshold, otherwise None - retry at a deeper threshold
    """
    twist_table = tables.twist_table
    flip_table = tables.flip_table
    slice_table = tables.flip_table

    lower_bound = max(tables.twist_slice_table[pack_twist(twist, slice_coord)], 
                      tables.flip_slice_table[pack_flip(flip, slice_coord)])

    movecount = len(path)
    if movecount + lower_bound > threshold:
        return None

    if twist == 0 and flip == 0 and slice_coord == 0:
        return path # Found a Phase 1 solution


    for m in range(N_MOVES):
        face = m // 3
        if face == last_face:
            continue

        new_twist = twist_table[twist][m]
        new_flip = flip_table[flip][m]
        new_slice = slice_table[slice_coord][m]

        result = phase1_search(new_twist, new_flip, new_slice, path + [m], threshold, face, tables)

        if result is not None:
            return result

    return None


def phase1_search_all(twist, flip, slice_coord, path, threshold, last_face, tables, deadline=None):
    """
    Like phase1_search, but yields every phase 1 solution found within the threshold instead of stopping at the first; solve() can try Phase 2 against several different states in G1
    Stops generating once the deadline passes
    """
    if deadline is not None and time.time() > deadline:
        return

    twist_table = tables.twist_table
    flip_table = tables.flip_table
    slice_table = tables.slice_table

    lower_bound = max(tables.twist_slice_table[pack_twist(twist, slice_coord)], 
                        tables.flip_slice_table[pack_flip(flip, slice_coord)])

    if len(path) + lower_bound > threshold:
        return

    if twist == 0 and flip == 0 and slice_coord == 0:
        yield path
        return # Don't explore past a path that already solved Phase 1

    for m in range (N_MOVES):
        face = m // 3
        if face == last_face:
            continue
        new_twist = twist_table[twist][m]
        new_flip = flip_table[flip][m]
        new_slice = slice_table[slice_coord][m]
        yield from phase1_search_all(new_twist, new_flip, new_slice, path + [m], threshold, face, tables, deadline)


def solve_phase1(cube, tables):
    """
    Find a shortest Phase 1 solution for the given cube by running phase1_search with an increasing movecount threshold
    Returns move list for the first/shortest threshold that succeeds
    """
    twist =  get_twist(cube)
    flip = get_flip(cube)
    slice_coord = get_slice_coord(cube)

    for threshold in range(21):
        result = phase1_search(twist, flip, slice_coord, [], threshold, -1, tables)

        if result is not None:
            return result

    return None # Should not happen for a legal cube


##### Phase 2 search/solve #####
def phase2_search(corners, ud_edges, slice_sorted_p2, path, threshold, last_face, tables, deadline=None):
    """
    Recursive IDA (iterative deepening) search for a Phase 2 solution within a given movecount threshold
    Gives up (returns None) once deadline passes
    """
    if deadline is not None and time.time() > deadline:
        return None

    corners_table = tables.corners_table
    ud_edges_table = tables.ud_edges_table
    slice_sorted_table = tables.slice_sorted_table

    lower_bound = max(tables.corners_slice_table[pack_corners(corners, slice_sorted_p2)], 
                      tables.ud_edges_slice_table[pack_ud_edges(ud_edges, slice_sorted_p2)])

    if len(path) + lower_bound > threshold:
        return None

    if corners == 0 and ud_edges == 0 and slice_sorted_p2 == 0:
        return path

    for m in PHASE_2_MOVES:
        face = m // 3
        if face == last_face:
            continue

        new_corners = corners_table[corners][m]
        new_ud_edges = ud_edges_table[ud_edges][m]
        new_slice = slice_sorted_table[slice_sorted_p2][m]

        result = phase2_search(new_corners, new_ud_edges, new_slice, path + [m], threshold, face, tables, deadline)

        if result is not None:
            return result

    return None


def solve_phase2(cube, max_moves, tables, deadline=None):
    """
    Find a shortest Phase 2 solution for the given cube using at most max_moves moves
    Returns None if there isn't one within the budget or the deadline passes
    """
    corners = get_corners(cube)
    ud_edges = get_ud_edges(cube)
    slice_sorted_p2 = get_slice_sorted(cube) % 24 # Return only the sorted values (0-23)

    for threshold in range(max_moves +1):
        result = phase2_search(corners, ud_edges, slice_sorted_p2, [], threshold, -1, tables, deadline)

        if result is not None:
            return result

        if deadline is not None and time.time() > deadline:
            return None

    return None


##### Overall solve #####
# Fine tune the move counts for solutions by lowering target and increasing time_limit
def solve(cube, tables, target=20, time_limit=10, first_pass_max=25):
    """
    Full two-phase solve
    Find a solution quickly, then keep shortening it until it has target moves or fewer, or until time_limit seconds have passed
    Returns the best solution found or None if none was found in time
    """
    deadline = time.time() + time_limit
    twist = get_twist(cube)
    flip = get_flip(cube)
    slice_coord = get_slice_coord(cube)

    best = None
    max_total = first_pass_max

    phase1_threshold = 0
    while phase1_threshold <= max_total and time.time() < deadline:
        # Try Phase 1 solutions of all lengths
        for phase1_moves in phase1_search_all(twist, flip, slice_coord, [], phase1_threshold, -1, tables, deadline):
            if len(phase1_moves) != phase1_threshold:
                continue # A shorter one

            # Replay Phase 1 moves on a real cube to get Phase 2's starting state
            intermediate = CubieCube(cube.cp, cube.co, cube.ep, cube.eo)
            for m in phase1_moves:
                intermediate.apply_move(m)

            phase2_moves = solve_phase2(intermediate, max_total - len(phase1_moves), tables, deadline)
            if phase2_moves is not None:
                best = phase1_moves + phase2_moves
                if len(best) <= target:
                    return best
                max_total = len(best) -1 # Only accept a new solution that is shorter

            if time.time() > deadline:
                break
        phase1_threshold += 1
        
    return best