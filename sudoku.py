
import cv2


class Sudoku:
    def __init__(self, height, width, board, locations):
        assert height == width
        self.locations = locations
        self.size = height
        self.height = height
        self.width = width
        self.init = board
        self.board = board
        self.depth = 0

    def solve_backtrack(self):
        self.depth += 1
        if self.depth > 5000:
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
                digit = self.board[i][j]
                cv2.putText(puzzleImage, str(digit), (17+i*factor, 30+j*factor),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # for (cellRow, boardRow) in zip(self.locations, self.board):
        #     # loop over individual cell in the row
        #     for (box, digit) in zip(cellRow, boardRow):
        #         # unpack the cell coordinates
        #         startX, startY, endX, endY = box

        #         # compute the coordinates of where the digit will be drawn
        #         # on the output puzzle image
        #         textX = int((endX - startX) * 0.33)
        #         textY = int((endY - startY) * -0.2)
        #         textX += startX
        #         textY += endY

        #         # draw the result digit on the sudoku puzzle image
        #         cv2.putText(puzzleImage, str(digit), (textX, textY),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # show the output image
        cv2.imshow("Sudoku Result", puzzleImage)
