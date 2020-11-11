import constraint
import cv2


class Sudoku:
    def __init__(self, height, width, board):
        assert height == width
        self.size = height
        self.height = height
        self.width = width
        self.init = board
        self.board = board
        self.depth = 0

    def solve_backtrack(self):
        self.depth += 1
        if self.depth > 15000:
            return

        find = self.find_empty()
        if not find:
            self.show_result()
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self.board[row][col] = i
                # ret, frame = self.cap.read()
                # cv2.imshow("frame", frame)
                if self.solve_backtrack():
                    return True

                self.board[row][col] = 0

        return False

    def solve_constraint(self):

        problem = constraint.Problem()

        # letting VARIABLES 11 through 99 have an interval of [1..9]
        for i in range(1, 10):
            problem.addVariables(range(i * 10 + 1, i * 10 + 10), range(1, 10))

        # adding the constraint that all values in a row must be different
        # 11 through 19 must be different, 21 through 29 must be all different,...
        for i in range(1, 10):
            problem.addConstraint(constraint.AllDifferentConstraint(),
                                  range(i * 10 + 1, i * 10 + 10))

        # Also all values in a column must be different
        # 11,21,31...91 must be different, also 12,22,32...92 must be different,...
        for i in range(1, 10):
            problem.addConstraint(
                constraint.AllDifferentConstraint(), range(10 + i, 100 + i, 10))

        # The last rule in a sudoku 9x9 puzzle is that those nine 3x3 squares must have all different values,
        # we start off by noting that each square "starts" at row indices 1, 4, 7
        for i in [1, 4, 7]:
            # Then we note that it's the same for columns, the squares start at indices 1, 4, 7 as well
            # basically one square starts at 11, the other at 14, another at 41, etc
            for j in [1, 4, 7]:
                square = [10*i+j, 10*i+j+1, 10*i+j+2, 10 *
                          (i+1)+j, 10*(i+1)+j+1, 10*(i+1)+j+2, 10*(i+2)+j, 10*(i+2)+j+1, 10*(i+2)+j+2]
                # As an example, for i = 1 and j = 1 (bottom left square), the cells 11,12,13,
                # 21,22,23, 31,32,33 have to be all different
                problem.addConstraint(
                    constraint.AllDifferentConstraint(), square)

        # adding a constraint for each number on the board (0 is an "empty" cell),
        # Since they're already solved, we don't need to solve them
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    def const(variable_value, value_in_table=self.board[i][j]):
                        if variable_value == value_in_table:
                            return True

                    # Basically making sure that our program doesn't change the values already on the board
                    # By telling it that the values NEED to equal the corresponding ones at the base board
                    problem.addConstraint(const, [((i+1)*10 + (j+1))])

        solutions = problem.getSolutions()

        if len(solutions) == 0:
            return
        else:
            for i, j in solutions[0].items():
                self.board[i//10-1][i % 10-1] = j
            self.show_result()

    def valid(self, num, pos):

        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def print_board(self):
        table = ''
        cell_length = len(str(self.size))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(self.board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.width) * self.height + '+' + '\n'
            table += (('| ' + '{} ' * self.width) * self.height + '|').format(*[format_int.format(
                x) if x != 0 else ' ' * cell_length for x in row]) + '\n'
            if i == self.size - 1 or i % self.height == self.height - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.width) * self.height + '+' + '\n'
        print(table)

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)  # row, col

    def make_valid(self):

        for i in range(len(self.board[0])):
            track = [0 for _ in range(10)]
            for j in range(len(self.board[0])):
                if self.board[i][j] and track[self.board[i][j]]:
                    self.board[i][j] = 0
                else:
                    track[self.board[i][j]] = 1

        for i in range(len(self.board[0])):
            track = [0 for _ in range(10)]
            for j in range(len(self.board[0])):
                if self.board[j][i] and track[self.board[j][i]]:
                    self.board[j][i] = 0
                else:
                    track[self.board[j][i]] = 1

        for box_y in range(0, 3):
            for box_x in range(0, 3):
                track = [0 for _ in range(10)]
                for i in range(box_y*3, box_y*3 + 3):
                    for j in range(box_x * 3, box_x*3 + 3):
                        if self.board[i][j] and track[self.board[i][j]]:
                            self.board[i][j] = 0
                        else:
                            track[self.board[i][j]] = 1
        return True

    def show_result(self):
        puzzleImage = cv2.imread("./template.jpg")
        factor = 565//9
        for i in range(9):
            for j in range(9):
                digit = self.board[j][i]
                cv2.putText(puzzleImage, str(digit), (17+i*factor, 30+j*factor),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow("Sudoku Result", puzzleImage)
