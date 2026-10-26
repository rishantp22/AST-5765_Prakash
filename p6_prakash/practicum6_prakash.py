# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Practicum 6: Combining Frames and Data Image Analysis
# October 2026

# FIXED: 2026-10-26 - adapted the previous HW8 image-reduction
# code for Practicum 6 flat-field correction and image masking.

import os
import numpy as np
from astropy.io import fits


# Practicum 6 - Problem 1
# Function: disk


def disk(radius, center, shape):
    """Create a Boolean mask containing a filled disk.

    Parameters
    ----------
    radius : float
        Radius of the disk in pixels.

    center : tuple
        Disk center in (y, x) order.

    shape : tuple
        Output image shape in (y, x) order.

    Returns
    -------
    mask : ndarray of bool
        True for pixels whose centers lie within the disk
        and False elsewhere.
    """

    cy, cx = center
    ny, nx = shape

    y, x = np.indices(
        (ny, nx)
    )

    distance_squared = (
        (y - cy) ** 2
        +
        (x - cx) ** 2
    )

    mask = distance_squared <= radius ** 2

    return mask


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

# ============================================================
# Function: skycormednorm
# Homework 8 - Problem 2
# ============================================================

def skycormednorm(object_frame, normalized_sky, normregion=None):
    """Subtract a normalized sky frame from an object image.

    Parameters
    ----------
    object_frame : ndarray
        Two-dimensional dark-subtracted object image.

    normalized_sky : ndarray
        Two-dimensional normalized median sky image.

    normregion : tuple, optional
        Region used to calculate the normalization factor,
        in the form:

        ((y1, x1), (y2, x2))

        If None, the whole image is used.

    Returns
    -------
    corrected : ndarray
        Two-dimensional sky-subtracted object image.
    """

    # Here working with copies so the input arrays are not modified.
    obj = np.array(
        object_frame,
        dtype=np.float64,
        copy=True
    )

    sky = np.array(
        normalized_sky,
        dtype=np.float64,
        copy=True
    )

    if obj.ndim != 2 or sky.ndim != 2:
        raise ValueError(
            "object_frame and normalized_sky must both be 2D."
        )

    if obj.shape != sky.shape:
        raise ValueError(
            "object_frame and normalized_sky must have the same shape."
        )

    # Select the region used to determine the normalization
    # factor for this particular object frame.
    if normregion is None:

        normdata = obj

    else:

        (y1, x1), (y2, x2) = normregion

        normdata = obj[
            y1:y2,
            x1:x2
        ]

    if normdata.size == 0:
        raise ValueError(
            "The normalization region contains no pixels."
        )

    # This is the factor that was removed when making the
    # normalized frames in normmedcomb().
    normfactor = np.median(normdata)

    # Restore the normalized sky to the flux level appropriate
    # for this individual object image.
    denormalized_sky = sky * normfactor

    # Subtract the scaled sky without altering either input.
    corrected = obj - denormalized_sky

    return corrected

# Practicum 6 - Problem 1 test

print("Practicum 6 - Problem 1")

disk_test = disk(
    6.2,
    (12.3, 14.5),
    (25, 30)
)

print(
    "Disk test shape:",
    disk_test.shape
)

print(
    "Pixel [14, 14] =",
    disk_test[14, 14]
)

print(
    "Pixel [2, 1] =",
    disk_test[2, 1]
)

fits.writeto(
    "disktest.fits",
    disk_test.astype(np.uint8),
    overwrite=True
)

print(
    "Wrote: disktest.fits"
)

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


# Practicum 5 normalization-factor record


# As per the assignement the normalization factors also
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

# ============================================================
# Homework 8 - Problem 2
# ============================================================

print(
    "\nHomework 8 - Problem 2: Sky Correction"
)


# ------------------------------------------------------------
# Verify skycormednorm() does not modify its inputs
# ------------------------------------------------------------

test_object = objcube[0].copy()
test_sky = sky_13s_mednorm.copy()

_ = skycormednorm(
    objcube[0],
    sky_13s_mednorm,
    normregion=normregion
)

print(
    "Object input unchanged:",
    np.array_equal(
        test_object,
        objcube[0]
    )
)

print(
    "Sky input unchanged:",
    np.array_equal(
        test_sky,
        sky_13s_mednorm
    )
)


# ------------------------------------------------------------
# Create output cube
# ------------------------------------------------------------

noskycube = np.zeros(
    objcube.shape,
    dtype=np.float64
)


# ------------------------------------------------------------
# Apply sky correction to every object image
# ------------------------------------------------------------

for i in range(nobj):

    noskycube[i] = skycormednorm(
        objcube[i],
        sky_13s_mednorm,
        normregion=normregion
    )


print(
    "Sky-subtracted object cube shape:",
    noskycube.shape
)


# ------------------------------------------------------------
# Print required pixel in final object frame
# ------------------------------------------------------------

last_pixel = noskycube[
    -1,
    217,
    184
]

print(
    "Last frame pixel [217, 184] after sky subtraction =",
    last_pixel
)


# ------------------------------------------------------------
# Write only the final corrected object frame
# ------------------------------------------------------------

last_objhead = objhead.copy()

last_objhead.add_history(
    "Median dark subtracted."
)

last_objhead.add_history(
    "Normalized median sky subtracted."
)

last_objhead.add_history(
    "Sky normalization region: "
    "((225,225),(-225,-225))."
)


fits.writeto(
    "stars_13s_9_nosky.fits",
    noskycube[-1],
    header=last_objhead,
    overwrite=True
)


print(
    "Wrote: stars_13s_9_nosky.fits"
)

print(
    "\nHomework 8 complete."
)
# ==================================================================================================================================================================================
# Practicum 6 - Problem 2a
# Create the normalized flat field

print(
    "\nPracticum 6 - Problem 2a: Flat Field"
)


# ------------------------------------------------------------
#  Find lamp-on and lamp-off FITS files
# ------------------------------------------------------------

lamponfile = []
lampofffile = []

filelist = os.listdir(datadir)

for filename in filelist:

    if (
        "k_lampon_" in filename
        and filename.endswith(fext)
    ):
        lamponfile.append(
            filename[:-len(fext)]
        )

    elif (
        "k_lampoff_" in filename
        and filename.endswith(fext)
    ):
        lampofffile.append(
            filename[:-len(fext)]
        )


# Sorting filenames so the order is reproducible.
lamponfile.sort()
lampofffile.sort()


print(
    "Number of lamp-on frames:",
    len(lamponfile)
)

print(
    "Number of lamp-off frames:",
    len(lampofffile)
)


if len(lamponfile) == 0:
    raise RuntimeError(
        "No k_lampon FITS files were found."
    )

if len(lampofffile) == 0:
    raise RuntimeError(
        "No k_lampoff FITS files were found."
    )


# ------------------------------------------------------------
# Create lamp data cubes
# ------------------------------------------------------------

nlampon = len(lamponfile)
nlampoff = len(lampofffile)

lamponcube = np.zeros(
    (nlampon, ny, nx),
    dtype=np.float64
)

lampoffcube = np.zeros(
    (nlampoff, ny, nx),
    dtype=np.float64
)


# ------------------------------------------------------------
# Read the lamp-on images
# ------------------------------------------------------------

for i in range(nlampon):

    image, header = fits.getdata(
        datadir + lamponfile[i] + fext,
        header=True
    )

    lamponcube[i] = image

    # Save a header to use for the output flat.
    lamponhead = header.copy()


# ------------------------------------------------------------
# Read the lamp-off images
# ------------------------------------------------------------

for i in range(nlampoff):

    image, header = fits.getdata(
        datadir + lampofffile[i] + fext,
        header=True
    )

    lampoffcube[i] = image


print(
    "Lamp-on cube shape:",
    lamponcube.shape
)

print(
    "Lamp-off cube shape:",
    lampoffcube.shape
)


# ------------------------------------------------------------
# Median-combine lamp-on and lamp-off sets separately
# ------------------------------------------------------------

med_lampon = np.median(
    lamponcube,
    axis=0
)

med_lampoff = np.median(
    lampoffcube,
    axis=0
)


print(
    "Median lamp-on shape:",
    med_lampon.shape
)

print(
    "Median lamp-off shape:",
    med_lampoff.shape
)


# ------------------------------------------------------------
# Subtract median lamp-off from median lamp-on
# ------------------------------------------------------------

flat_raw = (
    med_lampon
    -
    med_lampoff
)


# ------------------------------------------------------------
# Normalize the flat using the same region as HW8
# ((225, 225), (-225, -225))
# ------------------------------------------------------------

(y1, x1), (y2, x2) = normregion

flat_norm_region = flat_raw[
    y1:y2,
    x1:x2
]

flat_norm_factor = np.median(
    flat_norm_region
)


print(
    "Flat normalization factor:",
    flat_norm_factor
)


if flat_norm_factor == 0.0:
    raise ValueError(
        "Flat normalization factor is zero."
    )


flat = (
    flat_raw
    /
    flat_norm_factor
)


# ------------------------------------------------------------
# Print required pixel
# ------------------------------------------------------------

print(
    "Flat pixel [217, 184] =",
    flat[217, 184]
)


# ------------------------------------------------------------
# Write flat.fits
# ------------------------------------------------------------

flathead = lamponhead.copy()

flathead.add_history(
    "Median lamp-off frame subtracted "
    "from median lamp-on frame."
)

flathead.add_history(
    "Flat normalized using region "
    "((225,225),(-225,-225))."
)


fits.writeto(
    "flat.fits",
    flat,
    header=flathead,
    overwrite=True
)


print(
    "Wrote: flat.fits"
)


# Practicum 6 - Problem 2b
# Apply flat field to sky-subtracted object data


print(
    "\nPracticum 6 - Problem 2b: Apply Flat Field"
)


# ------------------------------------------------------------
# Apply flat-field correction
# ------------------------------------------------------------

# Divide every sky-subtracted object frame by the same
# normalized 2D flat field. NumPy broadcasting applies the
# flat to all frames in the 3D cube.

# Identify usable flat-field pixels.
valid_flat = (
    np.isfinite(flat)
    &
    (flat != 0.0)
)

print(
    "Number of invalid/zero flat pixels:",
    np.size(flat) - np.count_nonzero(valid_flat)
)


# Start the corrected cube with NaN values.
# A NaN marks detector pixels where a valid flat-field
# correction cannot be calculated.
flatcube = np.full_like(
    noskycube,
    np.nan,
    dtype=np.float64
)


# Divide only where the flat-field value is valid.
np.divide(
    noskycube,
    flat,
    out=flatcube,
    where=valid_flat
)


print(
    "Flat-corrected cube shape:",
    flatcube.shape
)


# ------------------------------------------------------------
# Print pixel [217, 184] from every corrected frame
# ------------------------------------------------------------

print(
    "Pixel [217, 184] in all flat-corrected frames:"
)

print(
    flatcube[:, 217, 184]
)


# ------------------------------------------------------------
# Write the final corrected frame
# ------------------------------------------------------------

flat_objhead = objhead.copy()

flat_objhead.add_history(
    "Median dark subtracted."
)

flat_objhead.add_history(
    "Normalized median sky subtracted."
)

flat_objhead.add_history(
    "Normalized lamp flat applied."
)


fits.writeto(
    "stars_13s_9_flat.fits",
    flatcube[-1],
    header=flat_objhead,
    overwrite=True
)


print(
    "Wrote: stars_13s_9_flat.fits"
)

print(
    "\nPracticum 6 complete."
)