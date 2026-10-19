# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Practicum 5: Combining Frames and Infrared Sky Correction
# October 2026

# FIXED: 2026-10-18 - adapted previous image-reduction code
# for Practicum 5 normalized median combination.

import os
import numpy as np
from astropy.io import fits

# Function: normmedcomb


def normmedcomb(data, normregion=None):
    """Normalize and median-combine a 3D image cube.

    Parameters
    ----------
    data : ndarray
        Three-dimensional array with shape (nframe, ny, nx).
        The input array is not modified.

    normregion : tuple, optional
        Region used to calculate the normalization factor for
        each frame, in the form:

        ((y1, x1), (y2, x2))

        If None, the full 2D image is used.

    Returns
    -------
    mednorm : ndarray
        Two-dimensional normalized median-combined image.

    normfactors : ndarray
        One-dimensional array containing one normalization
        factor for each input frame.

    Examples
    --------
    >>> test = np.ones((3, 4, 4), dtype=float)
    >>> med, factors = normmedcomb(test)
    >>> factors
    array([1., 1., 1.])
    >>> med.shape
    (4, 4)
    """

    work = np.array(
        data,
        dtype=np.float64,
        copy=True
    )

    if work.ndim != 3:
        raise ValueError(
            "Input data must be a three-dimensional array."
        )

    # Select normalization region


    if normregion is None:

        # Default: use the entire image in every frame.
        normdata = work

    else:

        (y1, x1), (y2, x2) = normregion

        normdata = work[
            :,
            y1:y2,
            x1:x2
        ]

    # Making sure the requested region contains pixels.
    if normdata.shape[1] == 0 or normdata.shape[2] == 0:
        raise ValueError(
            "The normalization region contains no pixels."
        )

    # Calculate one normalization factor for each frame
    

    normfactors = np.median(
        normdata,
        axis=(1, 2)
    )

    if np.any(normfactors == 0.0):
        raise ValueError(
            "At least one normalization factor is zero."
        )

    # Normalize every complete frame


    # Reshape the 1D normalization-factor array from:
    #
    # (nframe,)
    #
    # to:
    #
    # (nframe, 1, 1)
    #
    # so NumPy broadcasting divides each frame by its own
    # normalization factor.
    normalized = (
        work /
        normfactors[:, np.newaxis, np.newaxis]
    )

    # Median-combine normalized frames


    mednorm = np.median(
        normalized,
        axis=0
    )

    return mednorm, normfactors

# Input configuration

datadir = "hw6_data/"
fext = ".fits"

# Normalization region specified in Practicum 5.
normregion = (
    (225, 225),
    (-225, -225)
)

# Required Practicum 5 output.
sky_output = "sky_13s_mednorm.fits"


# Reconstructing dark-subtracted object data from HW6


print("Reading HW6 data...")

objfile = []
darkfile = []

filelist = os.listdir(datadir)

for filename in filelist:

    if (
        "stars_13s_" in filename
        and filename.endswith(fext)
    ):
        objfile.append(
            filename[:-len(fext)]
        )

    elif (
        "dark_13s_" in filename
        and filename.endswith(fext)
    ):
        darkfile.append(
            filename[:-len(fext)]
        )


# Keep file ordering reproducible.
objfile.sort()
darkfile.sort()


if len(objfile) == 0:
    raise RuntimeError(
        "No stars_13s_ FITS files were found in "
        + datadir
    )

if len(darkfile) == 0:
    raise RuntimeError(
        "No dark_13s_ FITS files were found in "
        + datadir
    )


print(
    "Number of object frames:",
    len(objfile)
)

print(
    "Number of dark frames:",
    len(darkfile)
)


# Determine image dimensions


image_data, image_header = fits.getdata(
    datadir + objfile[0] + fext,
    header=True
)

ny, nx = image_data.shape

nobj = len(objfile)
ndark = len(darkfile)


print(
    "Image dimensions:",
    ny,
    "x",
    nx
)


# Create object and dark cubes


objcube = np.zeros(
    (nobj, ny, nx),
    dtype=np.float64
)

darkcube = np.zeros(
    (ndark, ny, nx),
    dtype=np.float64
)


# Populate object cube


for i in range(nobj):

    image, header = fits.getdata(
        datadir + objfile[i] + fext,
        header=True
    )

    objcube[i] = image

    # Save the first object's header for later output.
    if i == 0:
        first_objhead = header.copy()

    # Keep the final object's header as well.
    objhead = header


# Populate dark cube

for i in range(ndark):

    image, header = fits.getdata(
        datadir + darkfile[i] + fext,
        header=True
    )

    darkcube[i] = image
    darkhead = header


print(
    "Object cube shape:",
    objcube.shape
)

print(
    "Dark cube shape:",
    darkcube.shape
)


# Median-combine dark frames


meddark = np.median(
    darkcube,
    axis=0
)

print(
    "Median dark shape:",
    meddark.shape
)


# Dark subtract all object images

# Use NumPy broadcasting to subtract the same 2D dark image
# from every image in the 3D object cube.

objcube -= meddark


print(
    "Dark-subtracted object cube shape:",
    objcube.shape
)


# Practicum 5 - Problem 3

print(
    "\nPracticum 5 - Normalized Median Combination"
)

print(
    "Normalization region:",
    normregion
)


# A copy saved so that we can explicitly verify that
# normmedcomb() does not modify its input array.
objcube_before_norm = objcube.copy()


sky_13s_mednorm, normfactors = normmedcomb(
    objcube,
    normregion=normregion
)



# Verify that input cube was unchanged


input_unchanged = np.array_equal(
    objcube,
    objcube_before_norm
)

print(
    "Input cube unchanged by normmedcomb():",
    input_unchanged
)



#results


print(
    "\nNormalization factors:"
)

print(normfactors)


print(
    "\nNumber of normalization factors:",
    len(normfactors)
)


print(
    "Normalized median sky shape:",
    sky_13s_mednorm.shape
)

# Save normalized median sky FITS file


skyhead = objhead.copy()

skyhead.add_history(
    "Normalized median-combined sky frame."
)

skyhead.add_history(
    "Normalization region: "
    "((225,225),(-225,-225))."
)


fits.writeto(
    sky_output,
    sky_13s_mednorm,
    header=skyhead,
    overwrite=True
)


print(
    "Wrote:",
    sky_output
)


# ============================================================
# Practicum 5 normalization-factor record
# ============================================================

# The assignment asks that the normalization factors also
# appear in a comment or dummy string in the main program.
#
# After running this script once, paste the printed values
# between the triple quotes below.

normalization_factor_note = """
Normalization factors from Practicum 5:

[10864.0, 11057.0, 10536.0, 10558.5, 11046.0,
 10623.0, 9916.5, 9916.5, 9859.5]
"""

print(
    "\nPracticum 5 complete."
)