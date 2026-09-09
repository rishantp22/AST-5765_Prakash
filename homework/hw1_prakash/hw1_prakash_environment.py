# Rishant Prakash
# AST 5765C - Homework 1, installation verification
# Date: 2026-09-09
# Prepared and run with Codex assistance; see the course work log.
"""Report the interpreter and required package versions for HW1."""

import sys

import IPython
import matplotlib
import notebook
import numpy as np
import pandas as pd
import scipy

print("Homework 1, Problem 2: Python environment verification")
print("Python:", sys.version.split()[0])
print("Interpreter:", sys.executable)
print("NumPy:", np.__version__)
print("SciPy:", scipy.__version__)
print("Matplotlib:", matplotlib.__version__)
print("pandas:", pd.__version__)
print("IPython:", IPython.__version__)
print("Jupyter Notebook:", notebook.__version__)
print("All required imports succeeded.")
