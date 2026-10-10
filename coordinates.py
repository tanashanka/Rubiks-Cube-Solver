##### Describes the cube at the coordinate level; Phase 1 coord is a 3-tuple of (CorOri, EdgOri, UDSlice); Phase 2 is a 3-tuple of (CorPer, EdgPer, p2UDSlice) #####
from cube import CubieCube, Cor, Edg
from misc import c_nk, rotate_arr_left, rotate_arr_right
# from misc import c_nk, rotate_left, rotate_right # STILL TO BE WRITTEN

# coordlevel.htm, UDSliceCoord.htm, twophase.htm

slice_edge = [Edg.FR,Edg.FL,Edg.BL,Edg.BR]
u_d_edge = [Edg.UR,Edg.UF,Edg.UL,Edg.UB,Edg.DR,Edg.DF,Edg.DL,Edg.DB]


def get_twist(cube):
    """
    Read the cube's corner orientations and return a coordinate integer from 0-2186 (3^7-1)
    """
    coord = 0
    for i in range(Cor.UFR,Cor.DBR): # range 1-7; corner 8 not necessary, orientation is defined by 1-7, so does not carry extra info
        coord = 3 * coord + cube.co[i]
    return coord


# coordinate from get_twist fed into set_twist as twist
def set_twist(cube, twist):
    """
    Read the cube's twist value (0-2186) and write corner orientations into the cube.co array
    """
    twist_parity = 0 # Running total of orientations written into the cube
    for i in range(Cor.DBR - 1,Cor.UFR - 1, -1): # Start with DBL, unpacks get_twist coordinate starting from last packed
        cube.co[i] = twist % 3 # Twist of corner i is the last digit of twist integer in base 3
        twist_parity += cube.co[i] # Increment twist parity by value of corner i twist
        twist //= 3 # Cuts off last digit and prepares twist to be used for next corner
    cube.co[Cor.DBR] = ((3 - twist_parity % 3) % 3) # Derive DBR corner twist from other 7


def get_flip(cube):
    """
    Read the cube's edge orientations and return a coordinate integer from 0-2047 (2^11-1)
    """
    coord = 0
    for i in range(Edg.UR,Edg.BR): # range 1-11
        coord = 2 * coord + cube.eo[i]
    return coord


# coordinate from get_flip fed into set_flip as flip
def set_flip(cube, flip):
    """
    Read the cube's flip value (0-2048) and write edge orientations into the cube.eo array
    """
    flip_parity = 0
    for i in range(Edg.BR -1,Edg.UR -1, -1):
        cube.eo[i] = flip % 2 # Flip of edge i is the last digit of flip integer in base 2
        flip_parity += cube.eo[i] # Increments flip parity by value of edge i flip
        flip //= 2 # Cuts off last digit and prepares flip to be used for next edge
    cube.eo[Edg.BR] = ((2 - flip_parity % 2) % 2) # Derive BR edge flip from other 11


def get_slice_coord(cube):
    """
    Scan edge positions from BR to UR and create coordinate from 0-494 (C(12,4)) for the UD slice edges (not sorted)
    Phase 1 function
    """
    coord = 0
    k = 3
    for i in range(Edg.BR,Edg.UR -1,-1): # Scans through all edges backwards; backwards so coord with all edges in slice = 0
        if cube.ep[i] in slice_edge: # Checks if an edge at position i is a slice edge
            k -= 1 # If a slice edge is in slice, decrement k
            if k < 0: # All slice edges found
                break
        else:
            coord += c_nk(i,k) # If a slice edge is not in slice, add C(i,k) to coordinate
    return coord


# coordinate from get_slice_coord fed into set_slice_coord as coord
def set_slice_coord(cube, coord):
    """
    Read the cube's UD slice coordinate and write slice edge positions into the cube.ep array
    Phase 1 function
    """
    x = coord
    for i in Edg:
        cube.ep[i] = -1 # Set all edge positions to an unused number

    s = 3 # Slice edges
    for i in range(Edg.BR, Edg.UR -1, -1): # Set slice edges
        if x >= c_nk(i, s): # If coord >= C(n,s) (starting from BR) at position i, then C(n,s) must have been added during encoding; a non-slice edge must be there 
            x -= c_nk(i, s) # Decrease coordinate by C(n,s)
        else:
            cube.ep[i] = slice_edge[3 - s] # Assigns slice edges in order (arbitrary)
            s -= 1
            if s < 0:
                break

    o = 0 # Non-slice edges
    for i in Edg: # Set non-slice edges
        if cube.ep[i] == -1: # All edges not assigned are u/d edges
            cube.ep[i] = u_d_edge[o]
            o += 1


def get_slice_sorted(cube):
    """
    Get the permutation and location of the UD slice edge and return a coordinate from 0-11880 (495*4!) in phase 1 and 0-24 (4!) in phase 2
    Phase 2 function
    """
    location_coord = 0
    k = 3 # Slots with a UD slice edge
    u_d_slice_edges = [None] * 4
    for i in range(Edg.BR, Edg.UR -1, -1): # Scan edges backwards for UD slice edges
        if cube.ep[i] in slice_edge: # If UD slice edge in position i, assign it to position k in u_d_slice_edges (starting from last pos)
            u_d_slice_edges[k] = cube.ep[i]
            k -= 1
            if k < 0:
                break
        else:
            location_coord += c_nk(i,k)
    # Rank ordering of u_d_slice_edges against slice_edge to get coordinate
    sort_coord = 0
    for i in range(3, 0, -1): # Compare u_d_slice_edges againt slice_edge; only 3 values because if 3 are sorted then 4 are sorted
        cycles = 0 # Counts how many times the array has been rotated left
        while u_d_slice_edges[i] != slice_edge[i]: # Rotate the unranked members of the array left until u_d edge in position i is in its home position
            rotate_arr_left(u_d_slice_edges, 0, i)
            cycles += 1
        # Multiply sort_coord by # of possible values for cycle at a given i
        # Number of possible values for cycle decreases by 1 each time because # of sorted slots increases by 1 each time
        # Puts sort_coord as a multiple of cycles so adding cycles will cover every coordinate integer
        sort_coord = (i + 1) * sort_coord + cycles
    # Multiply location_coord by 24 to return a multiple of 24
    # sort_coord is from 0-23 (24 values), so adding to 24*location_coord will cover every (location,sort) pair with a unique integer
    return (24 * location_coord + sort_coord)


# coordinate from get_slice_sorted fed into set_slice_sorted as coord
def set_slice_sorted(cube, coord):
    """
    Read the cube's UD slice sorted coordinate and write slice edge positions into the cube.ep array
    Phase 2 function
    """
    location_coord, sort_coord = divmod(coord, 24) # Split coord into location_coord and sort_coord
    for i in Edg:
        cube.ep[i] = -1 # Set all edges to an unused number

    u_d_slice_edges = slice_edge[:]
    for i in range(1, 4): # Generate permutation from sort_coord
        sort_coord, cycles = divmod(sort_coord, i + 1) # Split sort_coord into sort_coord and cycles
        while cycles > 0: # Unpack cycles with rotate_arr_right
            rotate_arr_right(u_d_slice_edges, 0, i)
            cycles -= 1

    k = 3 # Number of slice edges
    for i in range(Edg.BR, Edg.UR -1, -1): # Search for slice edge backwards
        if location_coord - c_nk(i,k) >= 0: # If C(i,k) >= 0, slice edge can't be at position i
            location_coord -= c_nk(i,k)
        else:
            cube.ep[i] = u_d_slice_edges[k]
            k -= 1
            if k < 0:
                break

    o = 0 # Non-slice edges
    for i in Edg: # Set non-slice edges
        if cube.ep[i] == -1:
            cube.ep[i] = u_d_edge[o]
            o += 1


def get_corners(cube):
    """
    Read the cube's corner permutations and return a coordinate integer from 0-40319 (8!-1)
    """
    corner_order = list(cube.cp) # Create corner order list from cube.cp
    coord = 0
    for i in range(Cor.DBR, Cor.UFR, -1): # Stops at 1; index 0 will contribute nothing
        cycles = 0
        while corner_order[i] != i:
            rotate_arr_left(corner_order, 0, i)
            cycles += 1
        coord = (i + 1) * coord + cycles # Same coordinate math as sort_coord from get_slice_sorted
    return coord


# coordinate from get_corners fed into set_corners as coord
def set_corners(cube, coord):
    """
    Read the cube's get_corners coordinate and write corner positions into cube.cp array
    """
    corners_home = list(Cor)
    for i in range(1, 8):
        coord, cycles = divmod(coord, i + 1)
        while cycles > 0:
            rotate_arr_right(corners_home, 0, i)
            cycles -= 1

    for i in Cor: # Set corners
        cube.cp[i] = corners_home[i]


def get_ud_edges(cube):
    """
    Read the cube's edge permutation and return an integer from 0-40319 (8!-1) 
    Phase 2 function
    """
    edge_order = list(cube.ep[0:8])
    coord = 0
    for i in range(Edg.DB, Edg.UR, -1): # Stops at 1l index 0 will contribute nothing
        cycles = 0
        while edge_order[i] != i:
            rotate_arr_left(edge_order, 0, i)
            cycles += 1
        coord = (i + 1) * coord + cycles # Same coordinate math as sort_coord from get_slice_sorted
    return coord


def set_ud_edges(cube, coord):
    """
    Reads the cub'e get_ud_edges coordinate and write corner positions into cube.ep array
    """
    edges_home = list(Edg)[0:8]
    for i in range(1, 8):
        coord, cycles = divmod(coord, i + 1)
        while cycles > 0:
            rotate_arr_right(edges_home, 0, i)
            cycles -= 1

    for i in range(Edg.UR, Edg.DB +1): # Set UD edges
        cube.ep[i] = edges_home[i]