# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Homework 9: Photometry Setup
# October 26, 2026

# FIXED: 2026-10-26 - adapted the previous HW8 image-reduction
# workflow and Practicum 6 flat-field correction for HW9 photometry.

import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import gaussian as g
from scipy.ndimage import median_filter

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
# ================================================================================================================================================================================================================================================
# Homework 9 - Problem 2
# Stellar photometry table


print(
    "\nHomework 9 - Problem 2: Photometry Table"
)

# Stellar photometry:
#                  yguess, xguess, width,  cy,     cx,     star,   sky
photometry = np.array([
    # star 0
    [
        [698, 512, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 0
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]   # frame 2
    ],

    # star 1
    [
        [668, 520, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 0
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]   # frame 2
    ],

    # star 2
    [
        [568, 283, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 0
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]   # frame 2
    ]
], dtype=float)


print(
    "Photometry table shape:",
    photometry.shape
)

print(
    "\nInitial photometry table:"
)

print(photometry)

# ============================================================
# Homework 9 - Problem 2
# Star 0 positions and dither offsets
# ============================================================

# Star 0 positions in frames 1 and 2 determined
# from inspection of the dithered images.

photometry[0, 1, 0] = 696
photometry[0, 1, 1] = 475

photometry[0, 2, 0] = 734
photometry[0, 2, 1] = 644


# Calculate offsets of star 0 between frames

dy01 = (
    photometry[0, 1, 0]
    -
    photometry[0, 0, 0]
)

dx01 = (
    photometry[0, 1, 1]
    -
    photometry[0, 0, 1]
)

dy02 = (
    photometry[0, 2, 0]
    -
    photometry[0, 0, 0]
)

dx02 = (
    photometry[0, 2, 1]
    -
    photometry[0, 0, 1]
)

print(
    "Frame 0 -> Frame 1 offset (dy, dx) =",
    (dy01, dx01)
)

print(
    "Frame 0 -> Frame 2 offset (dy, dx) =",
    (dy02, dx02)
)


# Apply the offsets to stars 1 and 2

nstar = photometry.shape[0]
nframe = photometry.shape[1]

for star in range(1, nstar):

    photometry[star, 1, 0] = (
        photometry[star, 0, 0]
        +
        dy01
    )

    photometry[star, 1, 1] = (
        photometry[star, 0, 1]
        +
        dx01
    )

    photometry[star, 2, 0] = (
        photometry[star, 0, 0]
        +
        dy02
    )

    photometry[star, 2, 1] = (
        photometry[star, 0, 1]
        +
        dx02
    )


print(
    "\nPhotometry table after applying dither offsets:"
)

print(photometry)

# Homework 9 - Problem 3a
# Fit 2D Gaussians to the three stars in the first three frames

print(
    "\nHomework 9 - Problem 3a: Gaussian Fits"
)


# Half-size of the square fitting region.
# Use an 11 x 11 subimage to estimate the local background.
fit_half_size = 5

nstar = photometry.shape[0]
nframe = photometry.shape[1]


for star in range(nstar):

    for frame in range(nframe):

        # ----------------------------------------------------
        # Approximate star position from Problem 2
        # ----------------------------------------------------

        yguess = int(
            round(
                photometry[
                    star,
                    frame,
                    0
                ]
            )
        )

        xguess = int(
            round(
                photometry[
                    star,
                    frame,
                    1
                ]
            )
        )


        # ----------------------------------------------------
        # Define subimage boundaries
        # ----------------------------------------------------

        ylow = yguess - fit_half_size
        yhigh = yguess + fit_half_size + 1

        xlow = xguess - fit_half_size
        xhigh = xguess + fit_half_size + 1


        # ----------------------------------------------------
        # Copy the subimage
        # ----------------------------------------------------

        # IMPORTANT:
        # .copy() prevents modification of the original
        # flat-corrected science image.

        subimage = flatcube[
            frame,
            ylow:yhigh,
            xlow:xhigh
        ].copy()


        # ----------------------------------------------------
        # Check that the subimage is valid
        # ----------------------------------------------------

        if subimage.shape != (
            2 * fit_half_size + 1,
            2 * fit_half_size + 1
        ):
            raise ValueError(
                "Subimage has unexpected shape for "
                f"star {star}, frame {frame}: "
                f"{subimage.shape}"
            )


        # ----------------------------------------------------
        # Estimate and subtract the background
        # ----------------------------------------------------

        background = np.nanmedian(
            subimage
        )

        subimage -= background


        # ----------------------------------------------------
        # Check for invalid pixels
        # ----------------------------------------------------

        if np.any(
            ~np.isfinite(subimage)
        ):
            raise ValueError(
                "Non-finite pixels found in fitting "
                f"subimage for star {star}, "
                f"frame {frame}."
            )


        # ----------------------------------------------------
        # Refine the starting position of the star
        # ----------------------------------------------------

        # Make a smoothed COPY only for finding the approximate
        # stellar center. The actual Gaussian fit below still
        # uses the original unsmoothed data.
        smooth_subimage = median_filter(
            subimage,
            size=3,
            mode="nearest"
        )

        # Search only near the expected center so that distant
        # stars or bad pixels do not determine the initial guess.
        search_half_size = 4

        search_y0 = fit_half_size - search_half_size
        search_y1 = fit_half_size + search_half_size + 1

        search_x0 = fit_half_size - search_half_size
        search_x1 = fit_half_size + search_half_size + 1

        search_region = smooth_subimage[
            search_y0:search_y1,
            search_x0:search_x1
        ]

        peak_relative = np.unravel_index(
            np.nanargmax(search_region),
            search_region.shape
        )

        peak_y = (
            search_y0
            +
            peak_relative[0]
        )

        peak_x = (
            search_x0
            +
            peak_relative[1]
        )

        print(
            f"Star {star}, frame {frame}: "
            f"refined initial center in subimage = "
            f"({peak_y}, {peak_x})"
        )


        # ----------------------------------------------------
        # Select pixels around the refined stellar position
        # ----------------------------------------------------

        coords = np.indices(
            subimage.shape,
            dtype=float
        )

        fit_radius = 3.0

        fitmask = (
            (
                (coords[0] - peak_y) ** 2
                +
                (coords[1] - peak_x) ** 2
            )
            <=
            fit_radius ** 2
        )

        fitmask &= np.isfinite(
            subimage
        )


        if np.count_nonzero(fitmask) < 15:
            raise ValueError(
                f"Too few valid fit pixels for "
                f"star {star}, frame {frame}."
            )


        # ----------------------------------------------------
        # Prepare coordinates for gaussian.py
        # ----------------------------------------------------

        yfit = subimage[
            fitmask
        ].reshape(
            1,
            -1
        )

        xfit = coords[
            :,
            fitmask
        ].reshape(
            2,
            1,
            -1
        )


        # ----------------------------------------------------
        # Initial Gaussian parameters
        # ----------------------------------------------------

        # Use the smoothed image only for the initial peak
        # estimate. This prevents a single hot pixel from
        # controlling the starting height.
        height_guess = smooth_subimage[
            peak_y,
            peak_x
        ]

        # Make sure the initial Gaussian amplitude is positive.
        if height_guess <= 0:
            height_guess = np.nanmax(
                search_region
            )


        fit_guess = (
            (1.0, 1.0),       # initial sigma_y, sigma_x
            (peak_y, peak_x), # refined initial center
            height_guess      # initial amplitude
        )


        # ----------------------------------------------------
        # Fit ORIGINAL unsmoothed stellar data
        # ----------------------------------------------------

        fw, fc, fh, err = g.fitgaussian(
            yfit,
            x=xfit,
            guess=fit_guess,
            lsargs={
                "maxfev": 10000
            }
        )


        # fw[0] = width in y
        # fw[1] = width in x
        #
        # fc[0] = center y within subimage
        # fc[1] = center x within subimage

        width_y = abs(fw[0])
        width_x = abs(fw[1])

        center_y_sub = fc[0]
        center_x_sub = fc[1]


        # ----------------------------------------------------
        # Average the two widths as requested
        # ----------------------------------------------------

        mean_width = np.mean(
            [
                width_y,
                width_x
            ]
        )


        # ----------------------------------------------------
        # Convert subimage coordinates back to full image
        # ----------------------------------------------------

        center_y_full = (
            ylow
            +
            center_y_sub
        )

        center_x_full = (
            xlow
            +
            center_x_sub
        )


        # ----------------------------------------------------
        # Store results in photometry table
        # ----------------------------------------------------

        # parameter 2 = width
        photometry[
            star,
            frame,
            2
        ] = mean_width

        # parameter 3 = fitted y center
        photometry[
            star,
            frame,
            3
        ] = center_y_full

        # parameter 4 = fitted x center
        photometry[
            star,
            frame,
            4
        ] = center_x_full


        # ----------------------------------------------------
        # Print individual fit result
        # ----------------------------------------------------

        print(
            f"Star {star}, frame {frame}: "
            f"width_y={width_y:.4f}, "
            f"width_x={width_x:.4f}, "
            f"mean_width={mean_width:.4f}, "
            f"cy={center_y_full:.4f}, "
            f"cx={center_x_full:.4f}"
        )


# ============================================================
# Print updated photometry table
# ============================================================

print(
    "\nPhotometry table after Gaussian fitting:"
)

print(photometry)

# Final photometry table from Gaussian fitting:
#
# Columns:
# yguess, xguess, width, cy, cx, star, sky
#
# [[[698. 512. 0.981325 698.613127 512.386238 nan nan]
#   [696. 475. 0.971110 696.157098 474.324616 nan nan]
#   [734. 644. 1.128465 734.006539 644.157795 nan nan]]
#
#  [[668. 520. 1.015028 667.880149 520.225937 nan nan]
#   [666. 483. 0.700254 667.367270 484.221753 nan nan]
#   [704. 652. 0.450926 703.497892 653.585845 nan nan]]
#
#  [[568. 283. 1.048050 568.258063 283.305867 nan nan]
#   [566. 246. 0.681239 566.497070 248.297787 nan nan]
#   [604. 415. 0.994091 603.470190 413.075365 nan nan]]]
#
# The fitted centers are reasonably consistent with the initial
# position guesses. Most differences are within a few pixels,
# which is expected because the initial coordinates were only
# approximate positions determined from the dither offsets.

# ============================================================
# Homework 9 - Problem 3b
# Global stellar width and photometry parameters
# ============================================================

print(
    "\nHomework 9 - Problem 3b: Photometry Parameters"
)


# Average all fitted stellar widths from the photometry table.
average_width = np.nanmean(
    photometry[:, :, 2]
)

print(
    "Average fitted stellar width =",
    average_width
)


# ------------------------------------------------------------
# Photometry aperture and sky-annulus parameters
# ------------------------------------------------------------

# A radius of 3 sigma contains nearly all of the flux of a
# Gaussian stellar profile while avoiding an unnecessarily
# large aperture.
aperture_radius = (
    3.0
    *
    average_width
)

# Start the sky annulus well outside the stellar profile.
sky_inner_radius = (
    5.0
    *
    average_width
)

# Use a wider outer radius to obtain enough pixels for a
# representative local background estimate.
sky_outer_radius = (
    8.0
    *
    average_width
)


# The subimage should contain the complete sky annulus with
# additional room around it. A width of about 20 sigma spans
# roughly +/-10 sigma around the stellar center.
subimage_size = int(
    np.ceil(
        20.0
        *
        average_width
    )
)

# Make the subimage size odd so there is a single central pixel.
if subimage_size % 2 == 0:
    subimage_size += 1


print(
    "Aperture radius =",
    aperture_radius
)

print(
    "Sky annulus inner radius =",
    sky_inner_radius
)

print(
    "Sky annulus outer radius =",
    sky_outer_radius
)

print(
    "Photometry subimage size =",
    subimage_size
)

# ============================================================
# Diagnostic plots for the 9 Gaussian fitting regions
# ============================================================

for star in range(nstar):

    for frame in range(nframe):

        yguess = int(round(photometry[star, frame, 0]))
        xguess = int(round(photometry[star, frame, 1]))

        ylow = yguess - fit_half_size
        yhigh = yguess + fit_half_size + 1

        xlow = xguess - fit_half_size
        xhigh = xguess + fit_half_size + 1

        checkimage = flatcube[
            frame,
            ylow:yhigh,
            xlow:xhigh
        ].copy()

        plt.figure(figsize=(5, 5))

        plt.imshow(
            checkimage,
            origin="lower",
            cmap="gray"
        )

        # Mark the expected center of the star.
        plt.axhline(
            fit_half_size,
            linestyle="--"
        )

        plt.axvline(
            fit_half_size,
            linestyle="--"
        )

        plt.title(
            f"Star {star}, Frame {frame}"
        )

        plt.xlabel("subimage x")
        plt.ylabel("subimage y")

        plt.savefig(
            f"hw9_fitcheck_star{star}_frame{frame}.png",
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()


print(
    "Wrote Gaussian fit diagnostic images."
)
# Homework 9 - Problem 2
# Inspect first three flat-corrected frames


for i in range(3):

    image = flatcube[i]

    vmin = np.nanpercentile(image, 5)
    vmax = np.nanpercentile(image, 99.8)

    plt.figure(figsize=(8, 8))

    plt.imshow(
        image,
        origin="lower",
        cmap="gray",
        vmin=vmin,
        vmax=vmax
    )

    plt.xlabel("x pixel")
    plt.ylabel("y pixel")

    plt.title(
        "Flat-corrected object frame "
        + str(i + 1)
    )

    plt.xlim(400, 650)
    plt.ylim(580, 780)

    plt.grid()

    plt.savefig(
        "hw9_frame"
        + str(i + 1)
        + "_star0_region.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()


print(
    "Wrote first-three-frame inspection plots."
)

# ============================================================
# Interactive check of star 0 position
# ============================================================

#for i in range(3):

    #image = flatcube[i]

    #vmin = np.nanpercentile(image, 5)
    #vmax = np.nanpercentile(image, 99.8)

    #plt.figure(figsize=(8, 8))

    #plt.imshow(
    #    image,
    #    origin="lower",
    #    cmap="gray",
    #    vmin=vmin,
    #    vmax=vmax
    #)

    #plt.xlabel("x pixel")
    #plt.ylabel("y pixel")

    #plt.title(
    #    "Frame "
    #    + str(i + 1)
    #    + ": click on star 0"
    #)

    #plt.xlim(400, 650)
    #plt.ylim(580, 780)

    #print(
    #    "\nFrame",
    #    i + 1,
    #    "- click once on star 0"
    #)

    #point = plt.ginput(
    #    1,
    #    timeout=-1
    #)

    #xclick, yclick = point[0]

    #print(
    #    "Clicked position (y, x) =",
    #    (yclick, xclick)
    #)

    #plt.close()