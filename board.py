

class Board():
    def __init__(self, rows, columns, square_size):
        self.rows = rows
        self.columns = columns
        self.square_size = square_size

    def __str__(self) -> str:
        return f"board {self.rows}x{self.columns}"