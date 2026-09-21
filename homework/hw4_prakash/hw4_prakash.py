# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Homework 4
# September 2026

import numpy as np
import matplotlib.pyplot as plt


print('Problem 2')

# Parameters for the Gaussian population.
mu = 55.0
sigma = 13.0
n_draws = 10000

# Problem 2(a): draw 10,000 random values from N(mu, sigma).
rng = np.random.default_rng(5765)
sample = rng.normal(loc=mu, scale=sigma, size=n_draws)

print('Number of draws =', n_draws)
print('Population mean =', mu)
print('Population standard deviation =', sigma)
print('Sample mean =', np.mean(sample))
print('Sample standard deviation =', np.std(sample, ddof=1))

# Problem 2(b): histogram from x = 0 to 100 with bin width 1.
bin_edges = np.arange(0.0, 101.0, 1.0)

plt.figure(figsize=(8.0, 5.5))
plt.hist(sample, bins=bin_edges, edgecolor='black')
plt.xlabel('x')
plt.ylabel('Number of Draws')
plt.title('Gaussian Random Sample: $\\mu = 55$, $\\sigma = 13$')
plt.tight_layout()
plt.savefig('hw4_prakash_problem2b_histogram.png', dpi=300)
plt.close()

# Problem 2(c): overplot the analytic Gaussian expectation.
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
bin_width = bin_edges[1] - bin_edges[0]

# Gaussian probability-density function evaluated at each bin center.
gaussian_pdf = (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(
    -0.5 * ((bin_centers - mu) / sigma) ** 2
)

# Expected number of draws per bin = N * PDF * bin width.
expected_counts = n_draws * gaussian_pdf * bin_width

plt.figure(figsize=(8.0, 5.5))
plt.hist(sample, bins=bin_edges, edgecolor='black', label='Random sample')
plt.plot(
    bin_centers,
    expected_counts,
    linewidth=2.0,
    label='Gaussian expectation'
)
plt.xlabel('x')
plt.ylabel('Number of Draws')
plt.title('Gaussian Sample and Analytic Distribution')
plt.legend()
plt.tight_layout()
plt.savefig('hw4_prakash_problem2c_gaussian_overlay.png', dpi=300)
plt.close()

print('Saved hw4_prakash_problem2b_histogram.png')
print('Saved hw4_prakash_problem2c_gaussian_overlay.png')


print('\nProblem 3')

print('''Problem 3(a): FWHM of a Gaussian

Start with the Gaussian function

    f(x) = A exp[-(x - mu)^2 / (2 sigma^2)].

At the peak, x = mu and f(mu) = A.  At half maximum,

    A/2 = A exp[-(x - mu)^2 / (2 sigma^2)].

Divide by A:

    1/2 = exp[-(x - mu)^2 / (2 sigma^2)].

Take the natural logarithm:

    ln(1/2) = -(x - mu)^2 / (2 sigma^2)

so

    (x - mu)^2 = 2 sigma^2 ln(2).

Therefore the two half-maximum points are

    x = mu +/- sigma sqrt(2 ln 2).

The full width between these two points is

    FWHM = 2 sigma sqrt(2 ln 2)
         = 2.35482 sigma
         ~= 2.354 sigma.
''')

print('''Problem 3(b): Meaning of a straight line on a log-log plot

Let a straight line on a log-log plot have slope m and intercept b:

    log10(y) = m log10(x) + b.

Exponentiating base 10 gives

    y = 10^[m log10(x) + b]
      = 10^b 10^[m log10(x)]
      = 10^b x^m.

Thus a straight line on a log-log plot represents a power law,

    y = A x^m,

where

    m = slope
    A = 10^b
    b = log10(A).

Equivalently, using natural logarithms,

    ln(y) = m ln(x) + b

corresponds to

    y = e^b x^m.
''')
