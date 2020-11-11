from sudoku import Sudoku
from board import build_board
import threading


class Solve(threading.Thread):
    def __init__(self, board, locations):
        self.game = board
        self.locations = locations

        threading.Thread.__init__(self)

    def run(self):
        puzzle = Sudoku(3, 3, board=self.game,
                        locations=self.locations)
        puzzle.make_valid()
        if sum([sum(i) for i in self.game]) > 10:
            puzzle.print_board()
            print("[INFO] solving sudoku puzzle...")
            puzzle.solve_backtrack()
            puzzle.print_board()
