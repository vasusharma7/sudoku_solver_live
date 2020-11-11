import cv2
from sudoku import Sudoku
from board import build_board
from thread import Solve
import argparse
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=False,
                help="backtrack or csp")
ap.add_argument("-i", "--image", required=False,
                help="path to image")
args = vars(ap.parse_args())
if args['image']:
    frame = cv2.imread(args['image'])
    board, cellLocs = build_board(frame)
    puzzle = Sudoku(3, 3, board=board)
    puzzle.make_valid()
    if sum([sum(i) for i in board]) > 10:
        puzzle.print_board()
        print("[INFO] solving sudoku puzzle...")
        if args['model'] == 'csp':
            print("Model : CSP")
            puzzle.solve_constraint()
            puzzle.print_board()
        else:
            print("Model : Backtracking")
            puzzle.solve_backtrack()
            puzzle.print_board()
        while True:
            if cv2.waitKey(1) & 0xFF == 27:
                break

else:
    cap = cv2.VideoCapture(0)
    counter = 1
    k = 1
    threads = []
    locations = []
    game = [[0]*9 for i in range(9)]
    while(True):
        # try:
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        try:
            print("[INFO] loading digit classifier...")
            print("[INFO] processing image...")
            board, cellLocs = build_board(frame)
            board = board.tolist()
            for i in range(len(board[0])):
                for j in range(len(board[0])):
                    if board[i][j] and (not game[i][j]):
                        game[i][j] = board[i][j]
        except:
            pass
        if not k % counter:
            obj = Solve(game)
            threads.append(obj)
            obj.run()
            game = [[0]*9 for i in range(9)]
            k = 0

        k += 1
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        # except:
        #     print(sys.exc_info()[0])
        #     break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
