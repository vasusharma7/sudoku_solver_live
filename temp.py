from PIL import Image
import pytesseract as pyt
img = Image.open(
    '/mnt/data/VIRUS/Projects/AI/opencv-sudoku-solver/output/temp1.png')
text = pyt.image_to_string(img, lang="eng")
print(text)
