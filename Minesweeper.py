import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.rows = 10
        self.columns = 10
        self.mines = 10
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(side='left')
        self.heatmap_var = tk.BooleanVar()
        self.create_widgets()
        self.place_mines()
        self.update_numbers()
        self.create_menu()
        self.adjust_window_size()

    def create_widgets(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for row in range(self.rows):
            for column in range(self.columns):
                button = tk.Button(self.grid_frame, width=2, height=1,
                                   command=lambda r=row, c=column: self.reveal(r, c))
                button.grid(row=row, column=column)
                self.grid[row][column] = {'button': button, 'mine': False, 'number': 0, 'revealed': False}

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            column = random.randint(0, self.columns - 1)
            if not self.grid[row][column]['mine']:
                self.grid[row][column]['mine'] = True
                mines_placed += 1

    def update_numbers(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if not self.grid[row][column]['mine']:
                    self.grid[row][column]['number'] = self.count_adjacent_mines(row, column)

    def count_adjacent_mines(self, row, column):
        count = 0
        for r in range(max(0, row-1), min(row+2, self.rows)):
            for c in range(max(0, column-1), min(column+2, self.columns)):
                if self.grid[r][c]['mine']:
                    count += 1
        return count

    def reveal(self, row, column):
        cell = self.grid[row][column]
        if cell['revealed']:
            return
        cell['revealed'] = True
        button = cell['button']
        if cell['mine']:
            button.config(text='●', fg='black')
            self.reveal_all()
            self.master.after(100, lambda: messagebox.showinfo("Game Over", "You clicked on a mine!"))
        else:
            button.config(text=cell['number'] if cell['number'] > 0 else '', bg='dark grey')
            if cell['number'] == 0:
                self.reveal_adjacent(row, column)
            self.check_win()

    def reveal_adjacent(self, row, column):
        for r in range(max(0, row-1), min(row+2, self.rows)):
            for c in range(max(0, column-1), min(column+2, self.columns)):
                if not self.grid[r][c]['revealed']:
                    self.reveal(r, c)

    def reveal_all(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                button = cell['button']
                if cell['mine']:
                    button.config(text='●', fg='black', bg='red')
                else:
                    button.config(text=cell['number'] if cell['number'] > 0 else '', bg='dark grey')
                cell['revealed'] = True

    def check_win(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                if not cell['mine'] and not cell['revealed']:
                    return
        self.reveal_all()
        self.master.after(100, lambda: messagebox.showinfo("Congratulations!", "You have won the game!"))
        raise Exception("This is an intentional error.")
    
    def reset_game(self):
        self.create_widgets()
        self.place_mines()
        self.update_numbers()
        self.adjust_window_size()

    def create_menu(self):
        menu_frame = tk.Frame(self.master)
        menu_frame.pack(side='right', fill='y', expand=True)

        difficulty_label = tk.Label(menu_frame, text="Difficulty:")
        difficulty_label.pack(pady=(10, 5))

        self.difficulty_var = tk.StringVar(value="Easy")
        difficulties = {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard", "Custom": "Custom"}
        for text, mode in difficulties.items():
            tk.Radiobutton(menu_frame, text=text, variable=self.difficulty_var, value=mode, command=self.toggle_custom_fields).pack(anchor='w')

        self.custom_frame = tk.Frame(menu_frame)
        self.custom_frame.pack(pady=(5, 10), fill='x', expand=True)

        tk.Label(self.custom_frame, text="Rows:").pack(side='left')
        self.row_entry = tk.Entry(self.custom_frame, width=5)
        self.row_entry.pack(side='left')

        tk.Label(self.custom_frame, text="Columns:").pack(side='left')
        self.column_entry = tk.Entry(self.custom_frame, width=5)
        self.column_entry.pack(side='left')

        tk.Label(self.custom_frame, text="Mines:").pack(side='left')
        self.mines_entry = tk.Entry(self.custom_frame, width=5)
        self.mines_entry.pack(side='left')

        start_button = tk.Button(menu_frame, text="Start", command=self.start_game)
        start_button.pack(pady=(10, 5))

        exit_button = tk.Button(menu_frame, text="Exit", command=self.master.destroy)
        exit_button.pack(pady=(5, 10))

        tk.Checkbutton(menu_frame, text="Heat Map", variable=self.heatmap_var, command=self.toggle_heat_map).pack()

        self.toggle_custom_fields()

    def toggle_heat_map(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                if not cell['revealed']:
                    self.update_button_color(row, column)

    def update_button_color(self, row, column):
        cell = self.grid[row][column]
        button = cell['button']
        if self.heatmap_var.get():
            danger_level = self.calculate_danger_level(row, column)
            color = self.get_color_for_danger_level(danger_level)
            button.config(bg=color)
        else:
            button.config(bg='SystemButtonFace')

    def calculate_danger_level(self, row, column):
        count = 0
        max_count = 0
        for r in range(max(0, row - 1), min(row + 2, self.rows)):
            for c in range(max(0, column - 1), min(column + 2, self.columns)):
                if self.grid[r][c]['mine']:
                    count += 1
                max_count += 1
        return count / max_count

    def get_color_for_danger_level(self, danger_level):
        if danger_level == 0:
            return 'green'
        elif danger_level <= 0.25:
            return 'yellow green'
        elif danger_level <= 0.50:
            return 'yellow'
        else:
            return 'red'

    def toggle_custom_fields(self):
        if self.difficulty_var.get() == "Custom":
            self.custom_frame.pack(pady=(5, 10), fill='x', expand=True)
        else:
            self.custom_frame.pack_forget()

    def start_game(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            self.rows, self.columns, self.mines = 10, 10, 10
        elif difficulty == "Medium":
            self.rows, self.columns, self.mines = 16, 16, 40
        elif difficulty == "Hard":
            self.rows, self.columns, self.mines = 16, 30, 99
        elif difficulty == "Custom":
            try:
                self.rows = int(self.row_entry.get())
                self.columns = int(self.column_entry.get())
                self.mines = int(self.mines_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid custom settings")
                return
        self.reset_game()

    def adjust_window_size(self):
        self.master.update()
        self.master.minsize(self.grid_frame.winfo_width() + 200, self.grid_frame.winfo_height())

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
