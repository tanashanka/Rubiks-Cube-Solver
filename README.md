# Rubik's Cube Solver

This is a Rubik's Cube solver written in Python. It implements Herbert Kociemba's **two-phase algorithm** (explained below), following his published description and reference implementation. The program is wrapped in a Tkinter interface where you can input either a scramble in cube notation or paint how the cube looks, and the program will output a set of moves to solve the cube.

![Scramble input](images/scrambleinput.png)
![Facelet input](images/faceletinput.png)

**[Download for Windows](https://github.com/tanashanka/Rubiks-Cube-Solver/releases)** (no Python needed)

Or run from source **python gui.py**

## Features
**Two ways to enter a cube:**
1. Type a scramble (U1, R2, F3 ...)
2. Paint the cube on a clickable unfolded net

**Cube Editor:** Starting from a blank cube or a solved cube, pick a color and click/drag across stickers to paint, right click to erase (center stickers are locked). Includes live counts of how many stickers of each color exist.

**Show scramble on cube:** Turn an inputted scramble into the cube it produces, then edit or solve it.

**Input checking:** Typos, wrong sticker counts, and impossible cubes (a single twisted corner/flipped edge, odd parity) are rejected with a message indicating the error.

**Standalone .exe** built with PyInstaller. Uses Python's standard library only; nothing to install.

![Blank cube](images/edgeflip.png)

## Using it
**Scramble Mode:** Enter moves separated by spaces. Each move is a face letter followed by a number from 1-3 (1 is a clockwise turn, 2 is a half-turn, and 3 is a counterclockwise turn). Faces are U, R, F, D, L, B.

**Cube Appearance Mode:** Click a color in the palette, then clock or drag over stickers to color them. The diagram is the standard unfolded net:
```
    U
  L F R B
    D
```

Regardless of input mode, the solution is shown in scramble notation with its length.

``R1 U2 F3 L3 U1 B2 D1 R3 F2 L2 R3 B1 D1 F2 U3 R2 U1 L2 B2 D1 (20f)``

## How it works
**Cube Model:** A cube state is represented in the program by the orientation and permutation of the 8 corners and 12 edges. Moves are composed with a group operation. The code rejects impossible cube states (wrong orientation totals or parity).

**Coordinates:** Each aspect of the cube is compressed into a single coordinate integer:

1. Corner twist - 2187 values (3^7)
2. Edge flip  - 2048 values (2^11)
3. Location of the 4 middle-slice edges - 495 values (12C4)
4. Order of the middle-slice edges - 24 values (4!)
5. Corner permutation - 40,320 values (8!)
6. Location of the other 8 edges - 40,320 values (8!)

Each cube state can be described using a unique combination of these coordinates.

**Move Tables:** For every coordinate and each of the 18 possible moves, the resulting coordinate is precomputed, so a move during the solving process is an array lookup rather than a cube operaiton.

**Pruning Tables:** A breadth-first search from the solved state over pairs of coordinate gives a lower bound on the moves needed to solve a given state, so the program can skip searching solutions with move counts lower than it.

**The Two-Phase Algorithm:** Phase 1 uses Iterative Deepening A* (IDA*) to reach a cube state in the subgroup G1 = <U, D, R2, L2, F2, B2> (all pieces are oriented and the middle-slice edges are in the middle-slice). Phase 2 solves the cube only using the moves in the subgroup so that it never leaves this subgroup which includes the solved state. The solver tries many phase-1 solutions of increasing move counts so that the combination of phase-1 + phase-2 moves is the lowest possible until it reaches the target length (20 moves) or the time limit (10 seconds).

## Results
Measured on 100 random 25-move scrambles:

XXX

The solver aims for a short solution quickly, not a provably optimal one.

## Project Layout
| File | Purpose |
|---|---|
|`cube.py`|Cube model, move composition, state validation|
|`coordinates.py`|Coordinate encodings and their inverses|
|`moves.py`|Move tables|
|`pruning.py`|Pruning tables (breadth-first search)|
|`build_tables.py`|Builds and caches all tables|
|`solver.py`|Two-phase IDA* searchwith a time limit|
|`face.py`, `notation.py`|Facelet-string and move-notation parsing, input checks|
|`solve_input.py`|Entry points from user text to a solution or an error message|
|`cube_grid.py`, `gui.py`|The Tkinter interface|

## Limitations
- Solutions are usually 20-22 moves; the solver does not find optimal solutions (any state on a 3x3 Rubik's Cube has been proven to have an optimal solution of 20 moves or less).
- The packaged build is Windows-only. From source is runs anywhere Python and Tkinter do.

## Credits
The two-phase algorithm is by Herbert Kociemba; see his write-up at [kociemba.org/math](https://kociemba.org/math/twophase.htm). This project follows his design and reference Python implementation, [RubikTwoPhase](https://github.com/hkociemba/RubiksCube-TwophaseSolver) (GPL-3.0): the coordinate encodings, table layouts, and facelet mappings come from that work. I wrote my own code structure and compared my solver's output against his.

What is different in this project:

- Pruning tables split into two smaller tables per phase, combined with max(), instead of symmetry-reduced combined tables
- Time-limited search that returns a first solution quickly and then shortens it
- The Tkinter interface
- Input checking and cube validation with readable error messages
- XXXXXXXXXXXXXXX TEST SUITE
- Windows .exe packaging

## License
This project is released under the GNU General Public Lecense v3.0 (see [`LICENSE`](LICENSE)), the same license as the reference implementation it follows.