# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Practicum 3: Fitting Data
# September 25, 2026

import numpy as np
import matplotlib.pyplot as plt
import linfit


# ============================================================
# Problem 1a: Read the two data sets and plot Model 1
# ============================================================

print("Problem 1a")

data = np.loadtxt("practicum3_1.dat")

x1 = data[:100, 0]
y1 = data[:100, 1]

x2 = data[100:, 0]
y2 = data[100:, 1]

plt.figure()
plt.scatter(x1, y1)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Practicum 3: Model 1 Data")
plt.savefig("practicum3_prakash_problem1a_model1.png",
            dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# Problem 1b: Linear fit to Model 1
# ============================================================

print("\nProblem 1b")

# The stated y uncertainty for each data point is 0.5.
sigma_y = 0.5

a1, b1, sa1, sb1, chisq1, prob1, covar1, yfit1 = \
    linfit.linfit(y1, x1, sigma_y)

print("For sigma_y = 0.5:")
print("Intercept =", a1, "+/-", sa1)
print("Slope     =", b1, "+/-", sb1)
print("Chi-square =", chisq1)
print("Probability of a worse chi-square =", prob1)

# The true line is y = 3.2*x + 1.2.
true_intercept = 1.2
true_slope = 3.2

print("\n3-sigma comparison with the true parameters:")
print("Intercept difference =", abs(a1 - true_intercept))
print("3 * intercept uncertainty =", 3.0 * sa1)
print("Slope difference =", abs(b1 - true_slope))
print("3 * slope uncertainty =", 3.0 * sb1)

if abs(a1 - true_intercept) <= 3.0 * sa1:
    print("The true intercept is within 3 sigma of the fitted intercept.")
else:
    print("The true intercept is NOT within 3 sigma.")

if abs(b1 - true_slope) <= 3.0 * sb1:
    print("The true slope is within 3 sigma of the fitted slope.")
else:
    print("The true slope is NOT within 3 sigma.")

# Compare fits for three different assumed uncertainties.
print("\nEffect of changing the assumed y uncertainty:")

for test_sigma in (0.2, 0.5, 0.9):
    a, b, sa, sb, chisq, prob, covar, yfit = \
        linfit.linfit(y1, x1, test_sigma)

    print("\nsigma_y =", test_sigma)
    print("Intercept =", a, "+/-", sa)
    print("Slope     =", b, "+/-", sb)
    print("Chi-square =", chisq)
    print("Probability =", prob)

print("\nBecause every point is assigned the same uncertainty, changing")
print("sigma_y does not change the best-fit slope and intercept.")
print("It does change their uncertainties, chi-square, and fit probability.")


# ============================================================
# Problem 1c: Goodness of fit and plot
# ============================================================

print("\nProblem 1c")

print("Probability of obtaining a worse chi-square by chance =", prob1)

xplot1 = np.linspace(np.min(x1), np.max(x1), 500)
yplot1 = a1 + b1 * xplot1

plt.figure()
plt.errorbar(x1, y1, yerr=sigma_y, fmt="o", label="Data")
plt.plot(xplot1, yplot1, label="Linear fit")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Practicum 3: Linear Fit to Model 1")
plt.legend()
plt.savefig("practicum3_prakash_problem1c_linear_fit.png",
            dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# Problem 1d: Try a linear fit on the quadratic data
# ============================================================

print("\nProblem 1d")

a2, b2, sa2, sb2, chisq2, prob2, covar2, yfit2 = \
    linfit.linfit(y2, x2, sigma_y)

print("Linear fit to Model 2:")
print("Intercept =", a2, "+/-", sa2)
print("Slope     =", b2, "+/-", sb2)
print("Chi-square =", chisq2)
print("Probability =", prob2)

print("\nThe linear model does not fit Model 2.")
print("Reason 1: the data have obvious curvature, so the residuals from")
print("a straight line are systematic rather than random.")
print("Reason 2: chi-square is extremely large and the probability of")
print("getting a worse chi-square is essentially zero.")

xplot2 = np.linspace(np.min(x2), np.max(x2), 500)
linear_plot2 = a2 + b2 * xplot2

plt.figure()
plt.errorbar(x2, y2, yerr=sigma_y, fmt="o", label="Data")
plt.plot(xplot2, linear_plot2, label="Linear fit")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Practicum 3: Linear Fit to Model 2")
plt.legend()
plt.savefig("practicum3_prakash_problem1d_bad_linear_fit.png",
            dpi=300, bbox_inches="tight")
plt.show()

# A quadratic model is appropriate for these data.
quad_coeff = np.polyfit(x2, y2, 2)
quad_yfit = np.polyval(quad_coeff, x2)

quad_chisq = np.sum(((y2 - quad_yfit) / sigma_y) ** 2)
quad_dof = y2.size - 3

# linfit returns a probability itself, but for this quadratic fit we use
# scipy's chi-square survival function.
from scipy.stats import chi2
quad_prob = chi2.sf(quad_chisq, quad_dof)

print("\nQuadratic fit coefficients [x^2, x, constant]:")
print(quad_coeff)
print("Quadratic chi-square =", quad_chisq)
print("Quadratic degrees of freedom =", quad_dof)
print("Quadratic fit probability =", quad_prob)

quad_plot = np.polyval(quad_coeff, xplot2)

plt.figure()
plt.errorbar(x2, y2, yerr=sigma_y, fmt="o", label="Data")
plt.plot(xplot2, quad_plot, label="Quadratic fit")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Practicum 3: Quadratic Fit to Model 2")
plt.legend()
plt.savefig("practicum3_prakash_problem1d_quadratic_fit.png",
            dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# Problem 2a: Create CCD-like data with 1% bad pixels
# ============================================================

print("\nProblem 2a")

# A fixed seed makes the practicum results reproducible.
rng = np.random.default_rng(5765)

good_pixels = rng.poisson(lam=10000.0, size=396)
bad_pixels = rng.uniform(low=0.0, high=1.0e6, size=4)

sample = np.concatenate((good_pixels, bad_pixels))

mean_original = np.mean(sample)
median_original = np.median(sample)

print("Original sample mean   =", mean_original)
print("Original sample median =", median_original)
print("The median is closer to 10000 because the extreme bad pixels")
print("pull the mean strongly but have much less effect on the median.")


# ============================================================
# Problem 2b: One round of 5-sigma clipping around the median
# ============================================================

print("\nProblem 2b")

std_original = np.std(sample)

mask = np.abs(sample - median_original) <= 5.0 * std_original
subsample = sample[mask]

print("Original standard deviation =", std_original)
print("Number of points before clipping =", sample.size)
print("Number of points after clipping  =", subsample.size)
print("Clipped mean   =", np.mean(subsample))
print("Clipped median =", np.median(subsample))
print("Clipped standard deviation =", np.std(subsample))

print("\nAfter clipping, the mean moves much closer to the median and")
print("the standard deviation decreases because extreme outliers are removed.")
