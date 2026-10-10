##### Face Ordering #####

FACE_NAMES = ['U', 'R', 'F', 'D', 'L', 'B']

def move_to_notation(m):
    """
    Convert a move index (0-17) into formal move notation
    """
    face = m // 3
    turn = m % 3 + 1 # Ex. X1, X2, X3
    return f"{FACE_NAMES[face]}{turn}"


def moves_to_notation(moves):
    """
    Combine moves into movelist string
    """
    return ' '.join(move_to_notation(m) for m in moves)



def notation_to_moves(notation_str):
    """
    Parse a string of moves in notation into a list of move indices
    """
    moves = []
    for move in notation_str.split():
        face_letter = move[0]
        turn = int(move[1]) # 1, 2, or 3
        face = FACE_NAMES.index(face_letter)
        moves.append(3 * face + (turn - 1))
    return moves


def check_scramble_text(scramble_text):
    """
    Check for mistakes in the written scramble and return message detailing errors.
    Returns None if the text is fine.
    """
    scramble_list = scramble_text.split()
    if not scramble_list:
        return "No scramble inputted"
    for move in scramble_list:
        if len(move) != 2:
            return f"'{move}' isn't a valid move. Each move is face letter and a number from 1 to 3."
        if move[0] not in ('U', 'R', 'F', 'D', 'L', 'B'):
            return f"'{move}' isn't a valid move. Faces are U, R, F, D, L, B."
        if move[1] not in ('1', '2', '3'):
            return f"'{move}' isn't a valid move. Use 1, 2, or 3 after the face (eg. U1, R2, F3)"
    return None