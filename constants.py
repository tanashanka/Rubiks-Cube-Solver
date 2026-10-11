from enum import IntEnum

N_TWIST = 2187 # 3^7
N_FLIP = 2048 # 2^11
N_SLICE = 495 # C(12,4)
N_SLICE_SORTED = 11880 # 495 * 24
N_SLICE_SORTED_P2 = 24 # 4!
N_CORNERS = 40320 # 8!
N_UD_EDGES = 40320 # 8!
N_MOVES = 18 # Total moves
PHASE_2_MOVES = [m for m in range(18) if m % 3 == 1 or m // 3 in (0,3)]
    # m % 3 == 1 picks out half-turn variants of each move
    # m // 3 in (0,3) picks out all 6 U and D moves


class Facelet(IntEnum):
    """
    Representation of the unfolded cube net as facelet names:
    
               | U1 U2 U3 |
               | U4 U5 U6 |
               | U7 U8 U9 |
    | L1 L2 L3 | F1 F2 F3 | R1 R2 R3 | B1 B2 B3 |
    | L4 L5 L6 | F4 F5 F6 | R4 R5 R6 | B4 B5 B6 |
    | L7 L8 L9 | F7 F8 F9 | R7 R8 R9 | B7 B8 B9 |
               | D1 D2 D3 |
               | D4 D5 D6 |
               | D7 D8 D9 |
    """
    U1 = 0
    U2 = 1
    U3 = 2
    U4 = 3
    U5 = 4
    U6 = 5
    U7 = 6
    U8 = 7
    U9 = 8
    R1 = 9
    R2 = 10
    R3 = 11
    R4 = 12
    R5 = 13
    R6 = 14
    R7 = 15
    R8 = 16
    R9 = 17
    F1 = 18
    F2 = 19
    F3 = 20
    F4 = 21
    F5 = 22
    F6 = 23
    F7 = 24
    F8 = 25
    F9 = 26
    D1 = 27
    D2 = 28
    D3 = 29
    D4 = 30
    D5 = 31
    D6 = 32
    D7 = 33
    D8 = 34
    D9 = 35
    L1 = 36
    L2 = 37
    L3 = 38
    L4 = 39
    L5 = 40
    L6 = 41
    L7 = 42
    L8 = 43
    L9 = 44
    B1 = 45
    B2 = 46
    B3 = 47
    B4 = 48
    B5 = 49
    B6 = 50
    B7 = 51
    B8 = 52
    B9 = 53


class Color(IntEnum):
    """
    Colors of the cube facelets
    'U' is the color of the U face, 'R' is the color of the R face, etc.
    Values used to identify individual faces as well
    """
    U = 0
    R = 1
    F = 2
    D = 3
    L = 4
    B = 5


class Corner(IntEnum):
    """
    Order of corner pieces
    """
    UFR = 0
    UFL = 1
    UBL = 2
    UBR = 3
    DFR = 4
    DFL = 5
    DBL = 6
    DBR = 7


class Edge(IntEnum):
    """
    Order of edge pieces
    """
    UR = 0
    UF = 1
    UL = 2
    UB = 3
    DR = 4
    DF = 5
    DL = 6
    DB = 7
    FR = 8
    FL = 9
    BL = 10
    BR = 11


class Move(IntEnum):
    """
    Face turns (Half-Turn Metric)
    """
    U1 = 0
    U2 = 1
    U3 = 2
    R1 = 3
    R2 = 4
    R3 = 5
    F1 = 6
    F2 = 7
    F3 = 8
    D1 = 9
    D2 = 10
    D3 = 11
    L1 = 12
    L2 = 13
    L3 = 14
    B1 = 15
    B2 = 16
    B3 = 17


class Symmetry(IntEnum):
    """
    All basic cube symmetries
    All 48 symmetries can be derived from these
    """
    ROT_URF3 = 0
    ROT_F2 = 1
    ROT_U4 = 2
    MIRR_LR2 = 3