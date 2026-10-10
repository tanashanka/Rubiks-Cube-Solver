##### Generate a random scramble #####
from cube import CubieCube
from random import randrange


def scramble(cube, n=25): # 25 moves is arbitrary
    """
    Apply 'n' moves to the given cube
    """
    moves = [randrange(18) for _ in range(n)]
    for m in moves:
        cube.apply_move(m) # Apply a random move 25 times
    return moves # List of moves
