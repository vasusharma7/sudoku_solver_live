<center><h1>Solving Sudoku on Live Cam</h1></center>

<center>This project is amalgamation of foundational Artificial Intelligence concepts - (Backtracking and CSP) and modern Machine Learning paradigms like Computer Vision (DL), along with some image processing and transformations</center>


 1. Detecting Sudoku
 
 - Used OpenCV Library to capture frames
 - For detecting Sudoku - 
 -  Invert the image
 -  Find horizontal and vertical lines
 -  Find various contours in the image
 -  Sort the contours in reverse order to find largest grid
 -  Find contours with 4 points (square)
 
 2. Detecting Digits
 
  - The location of each square on the board is located by calculating the length of each square on board which is trivial for a square

  - Used Deep Learning Model.
  - Trained the model on MNIST dataset of digits.
  - Used Keras with Tensorflow backend.
  
3. Solving Sudoku

    a. Used 2 Algorithms for this - 
    - Backtracking Search 
    - Based on Recursive DFS with sudoku constraints.
    - Takes long time on complex sudoku problems.

    b. Constraint Satisfaction Problem
     - Used Python py-constraint library for defining the problem and getting solution.
     - The sudoku problem has only 1 unique solution.
        *Can use either of them at a time - adjust in code.*



