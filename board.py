# USAGE
# python solve_sudoku_puzzle.py --model output/digit_classifier.h5 --image sudoku_puzzle.jpg

# import the necessary packages
from detect import extract_digit
from detect import find_puzzle
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True,
                    help="path to trained digit classifier")
    ap.add_argument("-i", "--image", required=True,
                    help="path to input sudoku puzzle image")
    ap.add_argument("-d", "--debug", type=int, default=-1,
                    help="whether or not we are visualizing each step of the pipeline")
    args = vars(ap.parse_args())
args = {}
args['debug'] = 0

path = "./models/digit_classifier.h5"
model = load_model(path)


def build_board(image):

    # load the input image from disk and resize it
    # image = cv2.imread('./puzzle.png')
    image = imutils.resize(image, width=600)

    # find the puzzle in the image
    (puzzleImage, warped) = find_puzzle(image, debug=args["debug"] > 0)
    # initialize our 9x9 sudoku board
    board = np.zeros((9, 9), dtype="int")

    # a sudoku puzzle is a 9x9 grid (81 individual cells), so we can
    # infer the location of each cell by dividing the warped image
    # into a 9x9 grid
    stepX = warped.shape[1] // 9
    stepY = warped.shape[0] // 9

    # initialize a list to store the (x, y)-coordinates of each cell
    # location
    cellLocs = []

    # loop over the grid locations
    for y in range(0, 9):
        # initialize the current list of cell locations
        row = []

        for x in range(0, 9):

            # compute the starting and ending (x, y)-coordinates of the
            # current cell
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY

            # add the (x, y)-coordinates to our cell locations list
            row.append((startX, startY, endX, endY))

            # crop the cell from the warped transform image and then
            # extract the digit from the cell
            try:
                cell = warped[startY:endY, startX:endX]
                digit = extract_digit(cell, debug=args["debug"] > 0)
            except:
                return []

            # verify that the digit is not empty
            if digit is not None:
                foo = np.hstack([cell, digit])
                # cv2.imshow("Cell/Digit", foo)

                # resize the cell to 28x28 pixels and then prepare the
                # cell for classification
                roi = cv2.resize(digit, (28, 28))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # classify the digit and update the sudoku board with the
                # prediction
                pred = model.predict(roi).argmax(axis=1)[0]
                board[y, x] = pred

        # add the row to our cell locations
        cellLocs.append(row)
    return board, cellLocs
