import cv2
from sudoku import Sudoku
from board import build_board
from thread import Solve
import sys
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
    frame = cv2.imread("./puzzle.png")
    cv2.imshow('frame', frame)

    try:
        print("[INFO] loading digit classifier...")
        print("[INFO] processing image...")
        board, cellLocs = build_board(frame)
        locations = cellLocs
        board = board.tolist()
        for i in range(len(board[0])):
            for j in range(len(board[0])):
                if board[i][j] and (not game[i][j]):
                    game[i][j] = board[i][j]
    except:
        pass
    if not k % counter:
        obj = Solve(game, locations)
        threads.append(obj)
        obj.run()
        game = [[0]*9 for i in range(9)]
        k = 0

    k += 1
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    break
    # except:
    #     print(sys.exc_info()[0])
    #     break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
