##### Create the input cube in the interface window #####
import tkinter as tk
from tkinter import ttk

FACE_ORDER = 'URFDLB'
COLORS = {'U': '#ffffff', 'R': '#d62828', 'F': '#2a9d3f', 
          'D': '#ffd60a', 'L': '#ff8c00', 'B': '#1d5fd6'}
BLANK = '#9e9e9e'
GOOD = '#1a7f37' # Text color when a count is right
BAD = '#c62828' # Text color when a count is wrong
CELL = 34 # Size of one sticker in pixels

# Top-left corner of each face in the unfolded net
#           U
#         L F R B
#           D
FACE_POSITION = {'U': (3,0), 'L': (0,3), 'F': (3,3), 'R': (6,3), 'B': (9,3), 'D': (3,6)}


class CubeGrid(ttk.Frame):
    """
    Shows the cube as an unfolded net. Pick a color in the, then left click stickers to paint them, right click to erase. Center stickers are fixed. Starts as a solved cube.
    Sticker i of facelet string is face FACE_ORDER[i // 9], row (i % 9) // 3, column i % 3.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.selected = 'U'
        self.stickers = [''] * 54 # '' = not painted yet
        self.items = [None] * 54 # Canvas rectangle for each sticker

        ## Six colors in palette, click one to select ##
        self.palette = tk.Canvas(self, width=6 * (CELL + 8) + 8, height=CELL + 16, highlightthickness=0)
        self.palette.pack(pady=(0,6))
        self.swatches = {}
        for i, letter in enumerate(FACE_ORDER):
            j = 8 + i * (CELL + 8)
            item = self.palette.create_rectangle(j, 8, j + CELL, 8 + CELL, fill=COLORS[letter], outline='black', width=1)
            self.swatches[item] = letter
            # letter=letter freezes this loop's value, otherwise every swatch would select 'B'
            self.palette.tag_bind(item, '<Button-1>', lambda event, letter=letter: self.select(letter))
        self.select('U')

        ## Unfolded cube ##
        self.cell_index = {} # (column, row) in the net -> sticker index, paintable stickers only
        self.canvas = tk.Canvas(self, width=12 * CELL + 2, height=9 * CELL + 2, highlightthickness=0)
        self.canvas.pack()
        for face_index, face in enumerate(FACE_ORDER):
            face_x, face_y = FACE_POSITION[face]
            for row in range(3):
                for column in range(3):
                    index = 9 * face_index + 3 * row + column
                    x = (face_x + column) * CELL + 1
                    y = (face_y + row) * CELL + 1
                    item = self.canvas.create_rectangle(x, y, x + CELL, y + CELL, fill=BLANK, outline='black')
                    self.items[index] = item
                    if row == 1 and column == 1:
                        # Center is always its own face letter, never painted
                        self.canvas.create_text(x + CELL // 2, y + CELL // 2, text=face, fill='white' if face in 'RFB' else 'black', font=('Arial', 12, 'bold'))
                    else:
                        self.cell_index[(face_x + column, face_y + row)] = index

        # One set of bindings on the whole canvas; pressing and dragging both paint
        # A drag keeps sending events to the widget where it started
        for press, motion, action in (('<Button-1>', '<B1-Motion>', self.paint),
                                      ('<Button-3>', '<B3-Motion>', self.erase)):
            self.canvas.bind(press, lambda event, action=action: self.act_at(event, action))
            self.canvas.bind(motion, lambda event, action=action: self.act_at(event, action))
    
        ## Live feedback on how many stickers of each color are painted ##
        counts = ttk.Frame(self)
        counts.pack(pady=(8,0))
        self.count_labels = {}
        for letter in FACE_ORDER:
            label = ttk.Label(counts, text='', width=7, anchor='center')
            label.pack(side='left', padx=2)
            self.count_labels[letter] = label
        self.unpainted_label = ttk.Label(self, text='')
        self.unpainted_label.pack()

        ## Buttons ##
        buttons = ttk.Frame(self)
        buttons.pack(pady=6)
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side='left', padx=5)
        ttk.Button(buttons, text="Solved cube", command=self.reset_solved).pack(side='left', padx=5)

        self.reset_solved() # Start with a solved cube

    ## Palette ##
    def select(self, letter):
        self.selected = letter
        for item, swatch_letter in self.swatches.items():
            self.palette.itemconfig(item, width=4 if swatch_letter == letter else 1)

    ## Painting ##
    def sticker_at(self, x, y):
        """
        Index of the paintable sticker at canvas point (x,y) or None (centers, gaps, outside)
        """
        return self.cell_index.get(((x - 1) // CELL, (y - 1) // CELL))

    def act_at(self, event, action):
        index = self.sticker_at(event.x, event.y)
        if index is not None:
            action(index)

    def paint(self, index):
        if self.stickers[index] == self.selected:
            return # Nothing would change; matters when dragging over the same sticker
        self.stickers[index] = self.selected
        self.refresh_sticker(index)

        self.refresh_counts()

    def erase(self, index):
        if self.stickers[index] == '':
            return
        self.stickers[index] = ''
        self.refresh_sticker(index)

        self.refresh_counts()

    def refresh_sticker(self, index):
        self.canvas.itemconfig(self.items[index], fill=COLORS.get(self.stickers[index], BLANK))

    def refresh_counts(self):
        for letter in FACE_ORDER:
            n = self.stickers.count(letter)
            self.count_labels[letter].config(text=f"{letter}: {n}/9", foreground=GOOD if n == 9 else BAD)
        blanks = self.blank_count()
        if blanks:
            plural = '' if blanks == 1 else 's'
            self.unpainted_label.config(text=f"{blanks} sticker{plural} not painted yet", foreground=BAD)
        else:
            self.unpainted_label.config(text="All stickers painted", foreground=GOOD)

    def refresh(self):
        for index in range(54):
            self.refresh_sticker(index)

        self.refresh_counts()

    @staticmethod
    def is_center(index):
        return index % 9 == 4

    ## Whole-grid operations ##
    def clear(self):
        """
        Blank every sticker except the centers
        """
        for index in range(54):
            self.stickers[index] = FACE_ORDER[index // 9] if self.is_center(index) else ''
        self.refresh()

    def reset_solved(self):
        self.stickers = [FACE_ORDER[index // 9] for index in range(54)]
        self.refresh()

    def set_string(self, text):
        """
        Fill the grid from a facelet string, centers stay fixed
        """
        for index, letter in enumerate(text.upper()[:54]):
            if self.is_center(index):
                continue
            self.stickers[index] = letter if letter in COLORS else ''
        self.refresh()

    ## Reading the grid ##
    def blank_count(self):
        """
        How many stickers have not been painted yet
        """
        return self.stickers.count('')

    def get_string(self):
        """
        Get the facelet string for what is on screen ('?' marks an unpainted sticker)
        """
        return ''.join(letter if letter else '?' for letter in self.stickers)

    def problem(self):
        """
        A message saying what is wrong with the painted colors, or None if every sticker is painted and there are 9 of each color.
        Does not check that the cube is possible
        """
        blanks = self.blank_count()
        if blanks:
            plural = '' if blanks == 1 else 's'
            return f"{blanks} sticker{plural} not painted yet."
        for letter in FACE_ORDER:
            n = self.stickers.count(letter)
            if n != 9:
                return f"There are {n} {letter} stickers. A cube has exactly 9 of each color."
        return None


if __name__ == "__main__":
    # Test window
    root = tk.Tk()
    root.title("Cube grid test")
    grid = CubeGrid(root)
    grid.pack(padx=10, pady=10)
    ttk.Button(root, text="Print string", command=lambda: print(grid.get_string())).pack(pady=(0, 10))
    root.mainloop()