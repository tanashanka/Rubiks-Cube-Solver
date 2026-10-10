##### Solves a cube based on user input scramble/state #####
from cube import CubieCube, verify
from face import from_facelet_string, check_facelet_text, to_facelet_string
from notation import notation_to_moves, moves_to_notation, check_scramble_text
from solver import solve


def solve_from_input(mode, text, tables):
    """
    mode: 'scramble' or 'facelet'
    Returns (solution_text, error_text). One of them is None.
    """
    text = text.strip().upper()

    if mode == 'scramble':
        error = check_scramble_text(text)
        if error:
            return None, error
        cube = CubieCube()
        for m in notation_to_moves(text):
            cube.apply_move(m)

    elif mode == 'facelet':
        text = ''.join(text.split())
        error = check_facelet_text(text)
        if error:
            return None, error
        cube = from_facelet_string(text)
        illegal = verify(cube)
        if illegal:
            return None, illegal

    else:
        return None, "Unknown input mode."

    solution = solve(cube, tables)
    if solution is None:
        return None, "Couldn't find a solution within the time limit."
    if not solution:
        return "The cube is already solved.", None

    return moves_to_notation(solution) + f" ({len(solution)}f)", None

def scramble_to_facelet(text):
    """
    Returns (facelet_string, error). One of them is None.
    """
    text = text.strip().upper()
    error = check_scramble_text(text)
    if error:
        return None, error
    cube = CubieCube()
    for m in notation_to_moves(text):
        cube.apply_move(m)
    return to_facelet_string(cube), None
