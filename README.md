<center><h1>Solving Sudoku on Live Cam</h1></center>

<center>This project is amalgamation of foundational Artificial Intelligence concepts - (Backtracking and CSP) and modern Machine Learning paradigms like Computer Vision (DL), along with some image processing and transformations</center>
<br/>

![Presentation](https://docs.google.com/presentation/d/1r9y4RNO1L54E_rSDBj7mjvv0h3xivp3G13jCqdWflWc/edit?usp=sharing)

**Requirements**
 
 1. Python
   - python3
   - pip3
  
 2. Packages
   - open-cv (cv2)
   - python-constraint
   - tensorflow
   - keras
   - numpy
   - scikit learn
   - imutils

**To run the project**

 - Run `python3 live.py` for starting webcam and start predicting.
 - Run `python3 live.py --image <path to image>` for recognizing and solving sudoku from image
 - Run `python3 live.py --image <path to image> --model <backtracking/csp>` for solving sudoku with a particular algorithm

Steps Involved - 


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

    Used 2 Algorithms for this - 
    
    a. Backtracking Search 
    - Based on Recursive DFS with sudoku constraints.
    - Takes long time on complex sudoku problems.

    b. Constraint Satisfaction Problem
     - Used Python py-constraint library for defining the problem and getting solution.
     - The sudoku problem has only 1 unique solution.
        *Can use either of them at a time - adjust in code.*



