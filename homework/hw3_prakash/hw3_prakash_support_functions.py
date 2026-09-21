"""Support functions for AST 5765 Homework 3.

This module contains functions for squaring numerical inputs and for plotting
the square function over an evenly spaced numerical range.
"""

import numpy as np
import matplotlib.pyplot as plt


def square(value):
    """Return the square of a numerical scalar or array.

    Parameters
    ----------
    value : array_like
        Numerical scalar or array of any dimension to be squared.

    Returns
    -------
    output : scalar or ndarray
        The element-by-element square of `value`.

    Examples
    --------
    >>> import numpy
    >>> square(numpy.array([1, 2, 3]))
    array([1, 4, 9])
    """
    return np.square(value)


def squareplot(low, high, npoints, saveplot=False):
    """Plot the square function over an evenly spaced numerical range.

    Parameters
    ----------
    low : int or float
        Low end of the range to plot.
    high : int or float
        High end of the range to plot. This endpoint is included.
    npoints : int
        Number of evenly spaced points between `low` and `high`.
    saveplot : str or bool, optional
        If not False, save the plot as a PDF using the supplied filename.
        The default is False.

    Returns
    -------
    None

    Examples
    --------
    >>> squareplot(1, 7, 5, saveplot='square_function.pdf')
    """
    x = np.linspace(low, high, npoints)

    y = square(x)

    plt.figure()
    plt.plot(x, y)
    plt.xlabel('Input')
    plt.ylabel('Output')
    plt.title('Square Function')

    if saveplot is not False:
        plt.savefig(saveplot, format='pdf', bbox_inches='tight')

    plt.close()