
# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Practicum 7: Photometry
# November 2026

import numpy as np


# ============================================================
# Problem 1 - Disk function from Practicum 6
# ============================================================

def disk(radius, center, shape):
    """Create a Boolean circular mask in (y, x) coordinates."""

    cy, cx = center
    y, x = np.indices(shape)

    return (y - cy)**2 + (x - cx)**2 <= radius**2


# ============================================================
# Problem 1 - Aperture photometry
# ============================================================

def apphot(image, mask, aperture_radius,
           sky_inner_radius, sky_outer_radius, center):
    """
    Perform aperture photometry on a 2D image.

    Parameters
    ----------
    image : ndarray
        Two-dimensional science image.
    mask : ndarray of bool
        True = good pixel; False = bad pixel.
    aperture_radius : float
        Radius of the stellar photometry aperture.
    sky_inner_radius : float
        Inner radius of the sky annulus.
    sky_outer_radius : float
        Outer radius of the sky annulus.
    center : tuple
        Stellar center in (y, x) order.

    Returns
    -------
    stellar_flux : float
        Background-subtracted aperture flux.
    average_sky : float
        Mean sky value per good annulus pixel.
    bad_pixels : int
        Number of bad pixels inside the aperture.
    """

    image = np.asarray(image, dtype=float)
    mask = np.asarray(mask, dtype=bool)

    if image.ndim != 2 or mask.shape != image.shape:
        raise ValueError("Image and mask must be matching 2D arrays.")

    if not (0 < aperture_radius < sky_inner_radius
            < sky_outer_radius):
        raise ValueError("Invalid aperture or sky annulus radii.")

    cy, cx = center
    ny, nx = image.shape

    # (a) Cut out a subimage large enough for the sky annulus.
    margin = int(np.ceil(sky_outer_radius)) + 2

    y0 = max(0, int(np.floor(cy)) - margin)
    y1 = min(ny, int(np.ceil(cy)) + margin + 1)
    x0 = max(0, int(np.floor(cx)) - margin)
    x1 = min(nx, int(np.ceil(cx)) + margin + 1)

    subimage = image[y0:y1, x0:x1].copy()
    submask = mask[y0:y1, x0:x1].copy()

    # Convert the full-image center to subimage coordinates.
    local_center = (cy - y0, cx - x0)

    # (b) Construct sky annulus using disk() twice.
    outer_disk = disk(
        sky_outer_radius, local_center, subimage.shape
    )
    inner_disk = disk(
        sky_inner_radius, local_center, subimage.shape
    )

    sky_annulus = outer_disk & ~inner_disk

    # Exclude bad and non-finite pixels.
    good_pixels = submask & np.isfinite(subimage)
    good_sky = sky_annulus & good_pixels

    if not np.any(good_sky):
        raise ValueError("No valid sky pixels in annulus.")

    # (c) Calculate average sky per pixel.
    average_sky = np.mean(subimage[good_sky])

    # (d) Subtract average sky from a COPY of the subimage.
    sky_subtracted = subimage - average_sky

    # (e) Construct the stellar aperture.
    aperture = disk(
        aperture_radius, local_center, subimage.shape
    )

    good_aperture = aperture & good_pixels

    # (f) Sum the background-subtracted stellar flux.
    stellar_flux = np.sum(sky_subtracted[good_aperture])

    # Bonus: count bad or non-finite pixels in the aperture.
    bad_pixels = int(np.count_nonzero(aperture & ~good_pixels))

    return stellar_flux, average_sky, bad_pixels



# ============================================================
# Problem 2 - Test aperture photometry
# ============================================================

print("\nPracticum 7 - Problem 2")

# Create a noiseless 21 x 21 Gaussian image.
ny, nx = 21, 21
y, x = np.indices((ny, nx))

sigma = 2.0
center = (10.0, 10.0)
amplitude = 1.0

gaussian_image = amplitude * np.exp(
    -(
        (y - center[0])**2 +
        (x - center[1])**2
    ) / (2 * sigma**2)
)

# All pixels are good in the synthetic test.
good_mask = np.ones(gaussian_image.shape, dtype=bool)

flux, sky, nbad = apphot(
    gaussian_image,
    good_mask,
    aperture_radius=6.0,
    sky_inner_radius=7.0,
    sky_outer_radius=10.0,
    center=center
)

print("Image shape:", gaussian_image.shape)
print("Gaussian sigma:", sigma)
print("Stellar flux:", flux)
print("Average sky:", sky)
print("Bad aperture pixels:", nbad)

# Total flux of a continuous 2D Gaussian.
theoretical_total = 2 * np.pi * amplitude * sigma**2

print("Theoretical total Gaussian flux:", theoretical_total)
print("\nPracticum 7 test complete.")
