# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Homework 3
# September 2026

import numpy as np
from hw3_prakash_support_functions import square, squareplot


print('Problem 2')

# Problem 2(h): create integers from 0 through 9 and square them.
test_square_1 = np.arange(10)
print('test_square_1 =')
print(test_square_1)
print('square(test_square_1) =')
print(square(test_square_1))

# Problem 2(i): create a 5 x 5 array of floats from 0 through 25.
test_square_2 = np.linspace(0.0, 25.0, 25).reshape(5, 5)
print('test_square_2 =')
print(test_square_2)
print('square(test_square_2) =')
print(square(test_square_2))


print('Problem 3')

# Five evenly spaced values from 1 to 7 are 1, 2.5, 4, 5.5, and 7.
squareplot(1, 7, 5, saveplot='hw3_prakash_problem3_plot.pdf')
print('Saved plot as hw3_prakash_problem3_plot.pdf')


print('Problem 4')
print('The rubric is submitted as hw3_prakash_problem4_rubric.txt.')