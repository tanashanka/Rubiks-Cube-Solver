##### Describes the cube at the facelet level #####
from cube import CubieCube
from constants import Facelet as Fc, Color as Col

FACE_NAMES = ['U', 'R', 'F', 'D', 'L', 'B']
# Map corner positions to facelet positions
cornerFacelet = [[Fc.U9, Fc.R1, Fc.F3], [Fc.U7, Fc.F1, Fc.L3], [Fc.U1, Fc.L1, Fc.B3], [Fc.U3, Fc.B1, Fc.R3],
                 [Fc.D3, Fc.F9, Fc.R7], [Fc.D1, Fc.L9, Fc.F7], [Fc.D7, Fc.B9, Fc.L7], [Fc.D9, Fc.R9, Fc.B7]]

# Map edge positions to facelet positions
edgeFacelet = [[Fc.U6, Fc.R2], [Fc.U8, Fc.F2], [Fc.U4, Fc.L2], [Fc.U2, Fc.B2], [Fc.D6, Fc.R8], [Fc.D2, Fc.F8],
               [Fc.D4, Fc.L8], [Fc.D8, Fc.B8], [Fc.F6, Fc.R4], [Fc.F4, Fc.L6], [Fc.B6, Fc.L4], [Fc.B4, Fc.R6]]

# Map corner positions to facelet colors
cornerColor = [['U', 'R', 'F'], ['U', 'F', 'L'], ['U', 'L', 'B'], ['U', 'B', 'R'], 
               ['D', 'F', 'R'], ['D', 'L', 'F'], ['D', 'B', 'L'], ['D', 'R', 'B']]

# Map edge positions to facelet colors
edgeColor = [['U', 'R'], ['U', 'F'], ['U', 'L'], ['U', 'B'], ['D', 'R'], ['D', 'F'], 
             ['D', 'L'], ['D', 'B'], ['F', 'R'], ['F', 'L'], ['B', 'L'], ['B', 'R']]


def to_facelet_string(cube):
    """
    Convert a CubieCube object into a facelet string
    """
    facelets = [''] * 54

    # Centers are fixed
    for i in range(6):
        facelets[(9 * i) + 4] = FACE_NAMES[i]

    # Corners
    for i in range(8):
        j = cube.cp[i]
        ori = cube.co[i]
        for k in range(3):
            facelets[cornerFacelet[i][(k + ori) % 3]] = cornerColor[j][k]

    # Edges
    for i in range(12):
        j = cube.ep[i]
        ori = cube.eo[i]
        for k in range(2):
            facelets[edgeFacelet[i][(k + ori) % 2]] = edgeColor[j][k]

    return ''.join(facelets)


def from_facelet_string(facelet_str):
    """
    Parse a 54-character facelet string into a CubieCube
    """
    cube = CubieCube()
    cube.cp = [-1] * 8 # Invalidate piece permutations
    cube.ep = [-1] * 12

    for i in range(8): # Corners
        face = cornerFacelet[i]
        for orientation in range(3): # If a facelet is U or D color, orientation corresponds to that facelet's orientation
            if facelet_str[face[orientation]] in ('U', 'D'):
                break
        color1 = facelet_str[face[(orientation + 1) % 3]] # The other 2 stickers, clockwise
        color2 = facelet_str[face[(orientation + 2) % 3]]
        for j in range(8):
            color = cornerColor[j]
            if color1 == color[1] and color2 == color[2]:
                cube.cp[i] = j
                cube.co[i] = orientation
                break

    for i in range(12): # Edges
        for j in range(12):
            if facelet_str[edgeFacelet[i][0]] == edgeColor[j][0] and \
                facelet_str[edgeFacelet[i][1]] == edgeColor[j][1]:
                cube.ep[i] = j
                cube.eo[i] = 0 # If stickers at position i match cubie j's stickers in the same order, then j is unflipped
                break
            if facelet_str[edgeFacelet[i][0]] == edgeColor[j][1] and \
                facelet_str[edgeFacelet[i][1]] == edgeColor[j][0]:
                cube.ep[i] = j
                cube.eo[i] = 1 # If they match but order swapped, edge is flipped
                break

    return cube


def check_facelet_text(facelet_text):
    """
    Check for mistakes in the written facelet list and return message detailing errors.
    Returns None if the text is fine.
    """
    if len(facelet_text) != 54:
        return f"Expected 54 characters, found {len(facelet_text)}."
    invalid = set(facelet_text) - set("URFDLB")
    if invalid:
        return f"Invalid characters: {', '.join(sorted(invalid))}. Use only U, R, F, D, L, B"
    for face in ('U', 'R', 'F', 'D', 'L', 'B'):
        if facelet_text.count(face) != 9:
            return f"'{face}' appears {facelet_text.count(face)} times. Expected 9 times."
    return None