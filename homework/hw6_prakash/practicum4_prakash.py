# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Practicum 4: Reading and Managing Imaging Data
# October 2, 2026

import os
import numpy as np
from astropy.io import fits


print("Problem 2")

# ============================================================
# Problem 2a
# ============================================================

# Hard-coded information is kept at the highest level.
datadir = "hw6_data/"
fext = ".fits"


# ============================================================
# Problem 2b
# ============================================================

objfile = []
darkfile = []

filelist = os.listdir(datadir)

for filename in filelist:

    # The supplied corrected files begin with "rdpharocor_",
    # so identify them by the relevant substring.
    if "stars_13s_" in filename and filename.endswith(fext):
        objfile.append(filename[:-len(fext)])

    elif "dark_13s_" in filename and filename.endswith(fext):
        darkfile.append(filename[:-len(fext)])


# Sort the files so their ordering is reproducible.
objfile.sort()
darkfile.sort()


# Give a clearer error if the expected files were not found.
if len(objfile) == 0:
    raise RuntimeError(
        "No stars_13s_ FITS files were found in " + datadir
    )

if len(darkfile) == 0:
    raise RuntimeError(
        "No dark_13s_ FITS files were found in " + datadir
    )


# ============================================================
# Problem 2c
# ============================================================

print("Data directory:", datadir)
print("FITS extension:", fext)
print("Last object file:", objfile[-1])
print("Last dark file:", darkfile[-1])


# ============================================================
# Problem 2d
# ============================================================

# Read one object image to determine the array dimensions.
image_data, image_header = fits.getdata(
    datadir + objfile[0] + fext,
    header=True
)

ny, nx = image_data.shape


# ============================================================
# Problem 2e
# ============================================================

nobj = len(objfile)
ndark = len(darkfile)

print("ny =", ny)
print("nx =", nx)
print("Number of object files =", nobj)
print("Number of dark files =", ndark)


print("\nProblem 3")

# ============================================================
# Problem 3a
# ============================================================

# Axis 0 = exposure number
# Axis 1 = y pixel
# Axis 2 = x pixel

objcube = np.zeros(
    (nobj, ny, nx),
    dtype=np.float64
)

darkcube = np.zeros(
    (ndark, ny, nx),
    dtype=np.float64
)

print("Object cube shape:", objcube.shape)
print("Dark cube shape:", darkcube.shape)


# ============================================================
# Problem 3b
# ============================================================

# Populate the object cube.
for i in range(nobj):

    image, header = fits.getdata(
        datadir + objfile[i] + fext,
        header=True
    )

    objcube[i] = image

    # Save the first object's header for later HW6 use.
    if i == 0:
        first_objhead = header.copy()

    # After the loop, objhead is the final object's header.
    objhead = header


# Populate the dark cube.
for i in range(ndark):

    image, header = fits.getdata(
        datadir + darkfile[i] + fext,
        header=True
    )

    darkcube[i] = image

    # After the loop, darkhead is the final dark header.
    darkhead = header


print("Last object DATE-OBS:", objhead["DATE-OBS"])
print("Last dark DATE-OBS:", darkhead["DATE-OBS"])


# ============================================================
# Problem 3c - Extra credit
# ============================================================

print("\nExtra-credit header information:")

print(
    "TIME-OBS keyword present in object header:",
    "TIME-OBS" in objhead
)

print("Object DATE-OBS:", objhead["DATE-OBS"])