import random

class SudokuGenerator:
    def __init__(self, difficulty="easy"):
      self.difficulty = difficulty
      self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def generate_sudoku(self):
        """Generates a Sudoku puzzle of a given difficulty."""
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        self.remove_cells()
        return self.grid

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        num = 0
        for i in range(3):
            for j in range(3):
                while True:
                    num = random.randint(1, 9)
                    if self.is_valid_in_box(row, col, num):
                        break
                self.grid[row + i][col + j] = num

    def is_valid_in_box(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if self.grid[row + i][col + j] == num:
                    return False
        return True

    def is_valid_in_row(self, row, num):
        for x in range(9):
            if self.grid[row][x] == num:
                return False
        return True

    def is_valid_in_col(self, col, num):
        for x in range(9):
            if self.grid[x][col] == num:
                return False
        return True

    def is_valid(self, row, col, num):
        return (
            self.is_valid_in_row(row, num)
            and self.is_valid_in_col(col, num)
            and self.is_valid_in_box(row - row % 3, col - col % 3, num)
        )

    def fill_remaining(self, i, j):
        if j >= 9 and i < 8:
            i += 1
            j = 0
        if i >= 9 and j >= 9:
            return True

        if i < 3:
            if j < 3:
                j = 3
        elif i < 6:
            if j == int(i / 3) * 3:
                j += 3
        else:
            if j == 6:
                i += 1
                j = 0
                if i >= 9:
                    return True

        for num in range(1, 10):
            if self.is_valid(i, j, num):
                self.grid[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.grid[i][j] = 0
        return False

    def remove_cells(self):
        # Adjust the number of cells to remove based on difficulty
        if self.difficulty == "easy":
            cells_to_remove = 40
        elif self.difficulty == "medium":
            cells_to_remove = 50
        else:
            cells_to_remove = 60

        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                cells_to_remove -= 1

def generate_sudoku(difficulty="easy"):
    generator = SudokuGenerator(difficulty)
    return generator.generate_sudoku()