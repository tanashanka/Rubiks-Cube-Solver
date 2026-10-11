from cube import CubieCube
from scramble import scramble
from build_tables import build_all_tables
from face import to_facelet_string
from solver import solve
from notation import moves_to_notation


tables = build_all_tables()

c = CubieCube()
scramble_moves = scramble(c, 25)
original = CubieCube(c.cp, c.co, c.ep, c.eo)
facelet_str = to_facelet_string(c)

print("Scramble:", scramble_moves)
print("Scramble notation:", moves_to_notation(scramble_moves))

solution = solve(c, tables, target=20, time_limit=10, first_pass_max=25)

print("Solution:", moves_to_notation(solution), f"({len(solution)}f)")