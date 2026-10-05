# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Homework 6: Median Combination
# October 2026

import os
import numpy as np
from astropy.io import fits


# ============================================================
# Input configuration
# ============================================================

datadir = "hw6_data/"
fext = ".fits"

dark_output = "dark_13s_med.fits"

# This filename is written exactly as requested in the HW6 handout.
object_output = "hw7_prakash_prob2_graph1.fits"


# ============================================================
# Read and organize input files
# ============================================================

objfile = []
darkfile = []

filelist = os.listdir(datadir)

for filename in filelist:

    if "stars_13s_" in filename and filename.endswith(fext):
        objfile.append(filename[:-len(fext)])

    elif "dark_13s_" in filename and filename.endswith(fext):
        darkfile.append(filename[:-len(fext)])


objfile.sort()
darkfile.sort()


if len(objfile) == 0:
    raise RuntimeError(
        "No stars_13s_ FITS files were found in " + datadir
    )

if len(darkfile) == 0:
    raise RuntimeError(
        "No dark_13s_ FITS files were found in " + datadir
    )


# Read one object image to determine array dimensions.
image_data, image_header = fits.getdata(
    datadir + objfile[0] + fext,
    header=True
)

ny, nx = image_data.shape

nobj = len(objfile)
ndark = len(darkfile)


# ============================================================
# Create and populate data cubes
# ============================================================

objcube = np.zeros(
    (nobj, ny, nx),
    dtype=np.float64
)

darkcube = np.zeros(
    (ndark, ny, nx),
    dtype=np.float64
)


for i in range(nobj):

    image, header = fits.getdata(
        datadir + objfile[i] + fext,
        header=True
    )

    objcube[i] = image

    if i == 0:
        first_objhead = header.copy()

    objhead = header


for i in range(ndark):

    image, header = fits.getdata(
        datadir + darkfile[i] + fext,
        header=True
    )

    darkcube[i] = image
    darkhead = header


print("Object cube shape:", objcube.shape)
print("Dark cube shape:", darkcube.shape)


# ============================================================
# Problem 2a - Median combine the dark images
# ============================================================

print("\nProblem 2a")

# np.median can combine the entire stack in one call.
# axis=0 collapses the exposure axis while retaining the
# y and x image dimensions.
meddark = np.median(
    darkcube,
    axis=0
)

print("Median dark shape:", meddark.shape)
print("Used np.median(darkcube, axis=0).")


# ============================================================
# Problem 2b
# ============================================================

print("\nProblem 2b")

print(
    "Median-dark pixel [217, 184] =",
    meddark[217, 184]
)


# ============================================================
# Problem 2c
# ============================================================

darkhead.add_history(
    "Median-combined dark frame."
)


# ============================================================
# Problem 2d
# ============================================================

fits.writeto(
    dark_output,
    meddark,
    header=darkhead,
    overwrite=True
)

print("Wrote:", dark_output)


# ============================================================
# Problem 2e
# ============================================================

# Save the requested first-frame pixel before subtraction.
pixel_before = objcube[0, 217, 184]

# NumPy broadcasting subtracts the 2D median dark from every
# image in the 3D object cube. No loop is required.
# The -= operator performs the subtraction in place.
objcube -= meddark

pixel_after = objcube[0, 217, 184]

print(
    "First object pixel [217, 184] before dark subtraction =",
    pixel_before
)

print(
    "First object pixel [217, 184] after dark subtraction =",
    pixel_after
)


first_objhead.add_history(
    "Median-combined 13 s dark frame subtracted."
)

fits.writeto(
    object_output,
    objcube[0],
    header=first_objhead,
    overwrite=True
)

print("Wrote:", object_output)