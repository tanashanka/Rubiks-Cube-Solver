##### Popout window for user interface #####
import queue
import threading
import tkinter as tk
from tkinter import ttk

from build_tables import build_all_tables
from solve_input import solve_from_input, scramble_to_facelet
from cube_grid import CubeGrid


class SolverWindow:
    def __init__(self, root): # root is the main window
        self.root = root
        root.title("Cube Solver")

        self.tables = None # Filled in once loading tables finishes
        self.results = queue.Queue() # Working threads put results here
        self.mode = tk.StringVar(value='scramble') # Linked to radio buttons
        self.grid = CubeGrid(root)

        # Mode choice: two radio buttons sharing self.mode
        mode_frame = ttk.Frame(root)
        ttk.Radiobutton(mode_frame, text="Scramble", variable=self.mode, value='scramble', command=self.update_hint).pack(side='left', padx=5)
        ttk.Radiobutton(mode_frame, text="Cube appearance", variable=self.mode, value='facelet', command=self.update_hint).pack(side='left', padx=5)
        
        # Hint, input, button, status, output
        self.hint = ttk.Label(root, text="", wraplength=450, justify='left')

        self.scramble_frame = ttk.Frame(root)
        self.input_box = tk.Text(self.scramble_frame, height=4, width=60)
        self.show_button = ttk.Button(self.scramble_frame, text="Show scramble on cube", command=self.on_show_scramble)
        self.input_box.pack()
        self.show_button.pack(pady=(4,0))

        self.solve_button = ttk.Button(root, text="Solve", command=self.on_solve, state='disabled')
        self.status = ttk.Label(root, text="Loading tables...")
        self.output_box = tk.Text(root, height=6, width=60, state='disabled')

        # Layout: pack() stacks widgets top to bottom in the order you call it
        mode_frame.pack(anchor='w', padx=10, pady=(10, 0))
        self.hint.pack(anchor='w', padx=10, pady=5)
        self.scramble_frame.pack(padx=10)
        self.solve_button.pack(pady=8)
        self.status.pack()
        self.output_box.pack(padx=10, pady=(5, 10))

        self.update_hint() # Show hint for the starting mode

        threading.Thread(target=self.load_tables, daemon=True).start()
        self.root.after(100, self.check_queue)

    ## Background work ##

    def load_tables(self):
        """
        Load tables in the background
        """
        try:
            self.results.put(('tables', build_all_tables(verbose=False)))
        except Exception as e: # Ends thread in case of exception instead of the window saying "Loading tables..." forever
            self.results.put(('load_error', str(e)))

    def run_solve(self, mode, text):
        try:
            solution, error = solve_from_input(mode, text, self.tables)
        except Exception as e:
            solution, error = None, f"Something went wrong: {e}"
        self.results.put(('result', solution, error)) # Posts 'result' tuple

    ## Main thread code ##

    def on_solve(self):
        """
        Runs when Solve is clicked
        """
        mode = self.mode.get() # Reads current mode and text from input box
        if mode == 'facelet':
            message = self.grid.problem()
            if message:
                self.show_output(message, is_error=True)
                return
            text = self.grid.get_string()
        else:
            text = self.input_box.get('1.0', 'end')
        self.solve_button.config(state='disabled') # No double clicks of Solve button while solving
        self.status.config(text="Solving...") # Update the status
        threading.Thread(target=self.run_solve, args=(mode, text), daemon=True).start() # Start run_solve in the background

    def check_queue(self):
        """
        Runs every 100ms on the main thread; picks up anything produced
        """
        try:
            while True: # Runs the whole queue, stops when Empty is raises
                item = self.results.get_nowait() # Take the next item off the queue without waiting; if queue is empty then raises queue.Empty
                if item[0] == 'tables': # Tables have loaded
                    self.tables = item[1] # Keep tables
                    self.status.config(text="Ready.") # Update status
                    self.solve_button.config(state='normal') # Enable Solve button
                elif item[0] == 'load_error': # Tables loading failed
                    self.status.config(text=f"Could not load tables: {item[1]}")
                elif item[0] == 'result': # Solve is finished
                    _, solution, error = item # Unpacks item
                    self.status.config(text="Ready.") # Update status
                    self.solve_button.config(state='normal') # Re-enable Solve button
                    self.show_output(solution if solution else error, is_error=bool(error)) # Pick whichever one of solution or error exists
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue) # Checks queue again 100ms later

    def show_output(self, text, is_error):
        """
        Enables the output box, clears it, inserts new text, and disables it again
        """
        self.output_box.config(state='normal')
        self.output_box.delete('1.0', 'end')
        self.output_box.insert('1.0', text)
        self.output_box.config(state='disabled', fg='red' if is_error else 'black')

    def update_hint(self):
        if self.mode.get() == 'scramble':
            self.grid.pack_forget()
            self.scramble_frame.pack(padx=10, before=self.solve_button)
            self.hint.config(text="Enter moves separated by spaces (eg. U1 R2 F3). The faces are U, R, F, D, L, B. The numbers are 1 (clockwise), 2 (half-turn), or 3 (counterclockwise)")
        else:
            self.scramble_frame.pack_forget()
            self.grid.pack(padx=10, before=self.solve_button)
            self.hint.config(text="Pick a color and click stickers to paint them. Right click erases. Centers are fixed.")

    def on_show_scramble(self):
        facelets, error = scramble_to_facelet(self.input_box.get('1.0', 'end'))
        if error:
            self.show_output(error, is_error=True)
            return
        self.grid.set_string(facelets)
        self.mode.set('facelet') # Radio button follows; shares variable
        self.update_hint()
        self.show_output("This is the cube after that scramble. Edit it, or press Solve.", is_error=False)

    
if __name__ == "__main__":
    root = tk.Tk() # Creates the main window
    SolverWindow(root)
    root.mainloop() # Starts event loop