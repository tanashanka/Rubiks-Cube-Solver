##### Describes the cube at the cubie level in terms of orientation and permutation of corners and edges #####
from constants import Color, Corner as Cor, Edge as Edg


##### Basic six moves described by piece permutations and changes in orientation #####
# U-move
cpU = [Cor.UBR, Cor.UFR, Cor.UFL, Cor.UBL, Cor.DFR, Cor.DFL, Cor.DBL, Cor.DBR] # corner permutations
coU = [0, 0, 0, 0, 0, 0, 0, 0] # changes in corner orientations
epU = [Edg.UB, Edg.UR, Edg.UF, Edg.UL, Edg.DR, Edg.DF, Edg.DL, Edg.DB, Edg.FR, Edg.FL, Edg.BL, Edg.BR] # edge permutations
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # changes in edge orientations

# R-move
cpR = [Cor.DFR, Cor.UFL, Cor.UBL, Cor.UFR, Cor.DBR, Cor.DFL, Cor.DBL, Cor.UBR]
coR = [2, 0, 0, 1, 1, 0, 0, 2]
epR = [Edg.FR, Edg.UF, Edg.UL, Edg.UB, Edg.BR, Edg.DF, Edg.DL, Edg.DB, Edg.DR, Edg.FL, Edg.BL, Edg.UR]
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# F-move
cpF = [Cor.UFL, Cor.DFL, Cor.UBL, Cor.UBR, Cor.UFR, Cor.DFR, Cor.DBL, Cor.DBR]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Edg.UR, Edg.FL, Edg.UL, Edg.UB, Edg.DR, Edg.FR, Edg.DL, Edg.DB, Edg.UF, Edg.DF, Edg.BL, Edg.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# D-move
cpD = [Cor.UFR, Cor.UFL, Cor.UBL, Cor.UBR, Cor.DFL, Cor.DBL, Cor.DBR, Cor.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Edg.UR, Edg.UF, Edg.UL, Edg.UB, Edg.DF, Edg.DL, Edg.DB, Edg.DR, Edg.FR, Edg.FL, Edg.BL, Edg.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# L-move
cpL = [Cor.UFR, Cor.UBL, Cor.DBL, Cor.UBR, Cor.DFR, Cor.UFL, Cor.DFL, Cor.DBR]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Edg.UR, Edg.UF, Edg.BL, Edg.UB, Edg.DR, Edg.DF, Edg.FL, Edg.DB, Edg.FR, Edg.UL, Edg.DL, Edg.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# B-move
cpB = [Cor.UFR, Cor.UFL, Cor.UBR, Cor.DBR, Cor.DFR, Cor.DFL, Cor.UBL, Cor.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Edg.UR, Edg.UF, Edg.UL, Edg.BR, Edg.DR, Edg.DF, Edg.DL, Edg.BL, Edg.FR, Edg.FL, Edg.UB, Edg.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
#################################################################################################################################

CUBE_OK = True # Verification for testing


class CubieCube:
    """
    Represents a cube by the permutations and orientaitons of its corner and edge cubies
    Also represents the 18 moves
    """
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        """
        Initialize corner/edge permutations/orientations
        cp: corner permutation
        co: corner orientation
        ep: edge permutation
        eo: edge orientation
        """
        if cp is None:
            self.cp = [Cor(i) for i in range(8)] # Builds the solved cube's corner permutation
        else:
            self.cp = cp[:] # Copies list from cp into self.cp
        if co is None:
            self.co = [0]*8 # List of 0s for all 8 corners
        else:
            self.co = co[:]
        if ep is None:
            self.ep = [Edg(i) for i in range(12)] # Builds the solved cube's edge permutation
        else:
            self.ep = ep[:]
        if eo is None:
            self.eo = [0]*12 # List of 0s for all 12 edges
        else:
            self.eo = eo[:]

    def __str__(self): # Debugging tool; prints corners/edges as (position,orientation)
        """
        Print position/orientation string for a cubie cube
        """
        s = ''
        for i in Cor(i):
            s = s + '(' + str(self.cp[i]) + ',' + str(self.co[i]) + ')'
        s = s + '\n'
        for i in Edg(i):
            s = s + '(' + str(self.ep[i]) + ',' + str(self.eo[i]) + ')'
        return s

    def __eq__(self, other): # Overloads == to compare cube states
        """
        Defines equality for cubie cubes
        """
        if self.cp == other.cp and self.co == other.co and self.ep == other.ep and self.eo == other.eo:
            return True
        else:
            return False

    def corner_multiply(self, b):
        """
        Multiply one cubie cube with another cubie cube, only corners
        """
        # self.cp[b.cp[i]] (Apply move self, then b):
        #   i = position in index
        #   b.cp[i] = corner in position i after b
        #   self.cp[b.cp[i]] = uses b.cp[i] as an index, corner c goes to position b.cp[i] according to self.cp
        # b.cp[i] = what position did the piece at i come from, self.cp[b.cp[i]] = the piece that was at that position when b was applied
        c_permutation = [0]*8 # Blank list
        c_orientation = [0]*8
        for i in range(8):
            c_permutation[i] = self.cp[b.cp[i]]
            c_orientation[i] = (self.co[b.cp[i]] + b.co[i]) % 3 # Corner orientation mod 3
        self.cp = c_permutation
        self.co = c_orientation

    def edge_multiply(self, b):
        """
        Multiply one cubie cube with another cubie cube, only edges
        """
        e_permutation = [0]*12
        e_orientation = [0]*12
        for i in range(12):
            e_permutation[i] = self.ep[b.ep[i]]
            e_orientation[i] = (self.eo[b.ep[i]] + b.eo[i]) % 2 # Edge orientation mod 2
        self.ep = e_permutation
        self.eo = e_orientation

    def multiply(self, b):
        """
        Multiply one cubie cube by another cubie cube
        """
        self.corner_multiply(b)
        self.edge_multiply(b)

    def inverse_cubie_cube(self, inv):
        """
        Computes the inverse of a cubie cube state; stores in 'inv' 
        """
        for e in Edg:
            inv.ep[self.ep[e]] = e # Doing inv on e followed by self on e results in e
        for e in Edg:
            inv.eo[e] = self.eo[inv.ep[e]]
        for c in Cor:
            inv.cp[self.cp[c]] = c
        for c in Cor:
            orientation = self.co[inv.cp[c]] # Orientation of self
            inv.co[c] = (-orientation)
            if inv.co[c] < 0:
                inv.co[c] += 3

    def apply_move(self, move): 
        """
        Convenience wrapper around multiply()
        """
        self.multiply(moveCube[move]) # moveCube defined below

    def is_solved(self):
        """
        Compares cubie cube against a solved cube
        """
        return self == CubieCube()
#########################################################################################################################################################

##### Cubes that represent the six basic moves #####

# Dictionary mapping each face name to an object representing one 90deg clockwise turn of that face
basicMoveCube = {
    Color.U: CubieCube(cpU, coU, epU, eoU),
    Color.R: CubieCube(cpR, coR, epR, eoR),
    Color.F: CubieCube(cpF, coF, epF, eoF),
    Color.D: CubieCube(cpD, coD, epD, eoD),
    Color.L: CubieCube(cpL, coL, epL, eoL),
    Color.B: CubieCube(cpB, coB, epB, eoB),
}

# Building all 18 moves from basic 6
moveCube = [None] * 18 # Empty list
for col in Color:
    cc = CubieCube()
    for k in range(3): # Runs loop 3 times, building up moves consisting of 1/2/3 quarter turns
        cc.multiply(basicMoveCube[col])
        moveCube[3 * col + k] = CubieCube(cc.cp, cc.co, cc.ep, cc.eo)


##########################################################################################################################################################


##### Parity/verification functions #####
def permutation_parity(permutation):
    """
    Number of swaps mod 2
    """
    swaps = 0
    for i in range(len(permutation)):
        for j in range(i + 1, len(permutation)):
            if permutation[i] > permutation[j]:
                swaps += 1
    return swaps % 2


def verify(cube):
    """
    Return None if the cube is legal, otherwise a message saying why not
    """
    if sorted(cube.cp) != list(range(8)):
        return "Some corners are missing or appear multiple times."
    if sorted(cube.ep) != list(range(12)):
        return "Some edges are missing or appear twice."
    if sum(cube.co) % 3 != 0:
        return "A corner is twisted."
    if sum(cube.eo) % 2 != 0:
        return "An edge is flipped."
    if permutation_parity(cube.cp) != permutation_parity(cube.ep):
        return "Two pieces are swapped."
    return None