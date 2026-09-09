# Rishant Prakash
# AST 5765C - Homework 2: Python practice
# Date: 2026-09-09
"""Solve HW2 with vectorized arrays and save both requested figures."""

from pathlib import Path

import matplotlib
import numpy as np

# Save figures without requiring a display on a Stokes compute node.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Paths stay inside this homework folder, even when run from elsewhere.
output_dir = Path(__file__).resolve().parent

print("Problem 1")
print("Rishant Prakash | AST 5765C | Homework 2 | 2026-09-09")
print("Main file: hw2_prakash.py in homework/hw2_prakash/.")
print("See the work log for setup, execution and submission status.")


print("\nProblem 2")
# Source for 2a-2d: NumPy Developers (2026), NumPy reference:
# https://numpy.org/doc/stable/reference/routines.array-creation.html
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html
# https://numpy.org/doc/stable/reference/generated/numpy.sin.html
# The upper limit of arange is exclusive; include integer 1000 by using 1001.
x = np.arange(0, 1001, dtype=np.int64)
print("2a1. Number of elements, including both endpoints:", x.size)
print("2a2. Integer array dtype:", x.dtype)
print("2a2. Minimum:", x.min(), "Maximum:", x.max())

# Retain x as the working array variable, promoting its dtype so fractional
# radians are representable. astype must allocate float storage; an integer
# ndarray cannot hold the requested rescaled values. Do not build a second
# sampling grid. The actual scaling below updates the promoted x in place.
x = x.astype(np.float64)
x *= 2. * np.pi / 1000.  # radians per original integer step
print("2b1. x was promoted to float64 and rescaled in place, in radians.")
print("2b2. Minimum:", x.min(), "Maximum:", x.max())
y = np.sin(x)
print("2c. y = sin(x) has", y.size, "dimensionless elements.")
print(f"2d. y[234] = {y[234]:.15f}")
print("Index 234 denotes the 235th element; the 234th is index 233.")


print("\nProblem 3")
# Source: Matplotlib Development Team (2026), Pyplot tutorial:
# https://matplotlib.org/stable/tutorials/pyplot.html
# Export reference: https://matplotlib.org/stable/api/_as_gen/
# matplotlib.pyplot.savefig.html (join the two preceding URL lines).
plt.rcParams.update({"font.size": 12, "axes.labelsize": 13,
                     "axes.titlesize": 14, "savefig.facecolor": "white",
                     "pdf.fonttype": 42})
fig_sine, ax_sine = plt.subplots(figsize=(7., 4.5), layout="constrained")
ax_sine.plot(x, y, color="#17638d", linewidth=2., label=r"$y=\sin(x)$")
ax_sine.set_xlabel(r"$x$ (radians)")
ax_sine.set_ylabel(r"$y=\sin(x)$ (dimensionless)")
ax_sine.set_title("Sine function over one period")
ax_sine.set_xlim(0., 2. * np.pi)
ax_sine.set_ylim(-1.12, 1.12)
ax_sine.set_xticks([0., 0.5 * np.pi, np.pi, 1.5 * np.pi, 2. * np.pi],
                  ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
ax_sine.axhline(0., color="0.55", linewidth=0.7, zorder=0)
ax_sine.grid(alpha=0.2)
ax_sine.legend(frameon=False, loc="upper right")
sine_path = output_dir / "hw2_prakash_problem3_sine.png"
fig_sine.savefig(sine_path, dpi=300)
plt.close(fig_sine)
print("3a. Plotted y against x with labeled axes and units.")
print("3b. Saved with Matplotlib:", sine_path.name)


print("\nProblem 4")
# Source: NumPy Developers (2026), linspace and clip reference:
# https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
# https://numpy.org/doc/stable/reference/generated/numpy.clip.html
# Keep the original ramp for the required comparison figure.
r = np.linspace(-1., 1., 101)
r_original = r.copy()
np.clip(r, -0.5, 0.5, out=r)
print("4a1. Original ramp:", r_original.size, "evenly spaced elements;")
print("minimum =", r_original.min(), "; maximum =", r_original.max())
print("spacing =", (r_original[-1] - r_original[0]) / (r_original.size - 1))
print("4a2. Clipped ramp minimum =", r.min(), "; maximum =", r.max())

fig_ramp, ax_ramp = plt.subplots(figsize=(7., 4.5), layout="constrained")
sample = np.arange(r.size)
ax_ramp.plot(sample, r_original, color="#17638d", linewidth=2.,
             label="Original ramp")
ax_ramp.plot(sample, r, color="#bd4e1b", linestyle="--", linewidth=2.2,
             label="Clipped to [-0.5, 0.5]")
ax_ramp.set_xlabel("Array index (zero based)")
ax_ramp.set_ylabel("Ramp value (dimensionless)")
ax_ramp.set_title("Original and clipped ramp")
ax_ramp.set_xlim(0, 100)
ax_ramp.set_ylim(-1.1, 1.1)
ax_ramp.grid(alpha=0.2)
ax_ramp.legend(frameon=False, loc="upper left")
ramp_path = output_dir / "hw2_prakash_problem4_ramp.pdf"
fig_ramp.savefig(ramp_path, metadata={"Title": "Original and clipped ramp",
                                     "Author": "Rishant Prakash"})
plt.close(fig_ramp)
print("4b. Saved both curves in one Matplotlib figure:", ramp_path.name)


print("\nProblem 5")
# Original paraphrases drafted with Codex assistance, not copied quotations.
# Sources: Astropy Developers (2026), Astropy 8.0.1 documentation;
# Photutils Developers (2026), Photutils 3.0.0 documentation, 17 April 2026.
# Both are community projects distributed freely outside UCF.
print('''Astropy - https://www.astropy.org/
Astropy is a free, open-source Python package that supplies common building
blocks for astronomical analysis. It can read and write FITS files, attach
physical units to quantities, transform celestial coordinates, and handle
astronomical times and tables. These tools help keep an analysis consistent
when data arrive with different units or coordinate conventions. For example,
an imaging workflow can read a FITS image and use its coordinate information
to relate image positions to positions on the sky. It is developed by the
Astropy community. Source: Astropy Developers (2026), Astropy 8.0.1 user
documentation, https://docs.astropy.org/en/stable/ (accessed 2026-09-09).

Photutils - https://photutils.readthedocs.io/en/stable/
Photutils is a free, open-source Python package for finding astronomical
sources and measuring their light in images. Its tools include estimating
the background, locating sources, measuring flux inside apertures, and
fitting point-spread-function models. For example, aperture photometry can
measure a star's signal after accounting for the surrounding background;
PSF fitting provides another way to measure sources when their images
overlap. Photutils works with the Astropy ecosystem and is maintained by
the Photutils developers. Source: Photutils Developers (2026), Photutils
3.0.0 documentation, dated 2026-04-17,
https://photutils.readthedocs.io/en/stable/ (accessed 2026-09-09).''')


print("\nProblem 6")
print("This run completed the numerical work and wrote both plot files.")
print("The work log records whether this run was local or on Stokes.")
print("Git, transfer and Stokes evidence must be checked in that log.")


print("\nProblem 7")
print("Upload the final Stokes-created tar.gz to Webcourses after verifying")
print("all required files. Running this program does not submit homework.")
