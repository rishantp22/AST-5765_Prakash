# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Homework 5: Probability and Error Analysis
# September 28, 2026

import numpy as np


def sigrej(data, rejection_limits, mask=None):
    """Return a Boolean mask after iterative sigma rejection.

    Parameters
    ----------
    data : array_like
        Numerical data to be sigma rejected.
    rejection_limits : tuple
        Number of standard deviations to use as the rejection limit
        at each iteration.  For example, ``(5.0, 5.0)`` performs
        two successive 5-sigma rejection steps.
    mask : array_like of bool, optional
        Boolean mask with the same shape as `data`.  True values are
        initially considered good and False values are excluded.
        If omitted, all points are initially considered good.

    Returns
    -------
    good_mask : ndarray of bool
        Modified Boolean mask.  True values are retained as good data;
        False values have been rejected.

    Examples
    --------
    >>> x = np.array([10.0, 10.1, 9.9, 1000.0])
    >>> sigrej(x, (1.5,))
    array([ True,  True,  True, False])
    """
    data = np.asarray(data)

    if mask is None:
        good_mask = np.ones(data.shape, dtype=bool)
    else:
        good_mask = np.asarray(mask, dtype=bool).copy()

        if good_mask.shape != data.shape:
            raise ValueError("mask must have the same shape as data")

    for limit in rejection_limits:
        good_data = data[good_mask]

        if good_data.size == 0:
            break

        mean = np.mean(good_data)
        std = np.std(good_data)

        if std == 0.0:
            break

        new_good = np.abs(data - mean) <= limit * std

        # Preserve any points that were already marked bad.
        good_mask = good_mask & new_good

    return good_mask


# ============================================================
# Problem 2: Continue the sigma clipping from Practicum 3
# ============================================================

print("Problem 2")

# Recreate the Practicum 3 data reproducibly.
rng = np.random.default_rng(5765)

good_pixels = rng.poisson(lam=10000.0, size=396)
bad_pixels = rng.uniform(low=0.0, high=1.0e6, size=4)

sample = np.concatenate((good_pixels, bad_pixels))

# Practicum 3 Problem 2b: first clipping step, within 5 sigma
# of the median.
median0 = np.median(sample)
std0 = np.std(sample)

mask1 = np.abs(sample - median0) <= 5.0 * std0
subsample = sample[mask1]

mean1 = np.mean(subsample)
median1 = np.median(subsample)
std1 = np.std(subsample)

print("After first 5-sigma clipping:")
print("Mean   =", mean1)
print("Median =", median1)
print("Std    =", std1)
print("Number of points =", subsample.size)

# Homework 5 Problem 2: repeat the clipping on the subsample.
median1_for_clip = np.median(subsample)
std1_for_clip = np.std(subsample)

mask2 = np.abs(subsample - median1_for_clip) <= 5.0 * std1_for_clip
subsubsample = subsample[mask2]

mean2 = np.mean(subsubsample)
median2 = np.median(subsubsample)
std2 = np.std(subsubsample)

print("\nAfter second 5-sigma clipping:")
print("Mean   =", mean2)
print("Median =", median2)
print("Std    =", std2)
print("Number of points =", subsubsample.size)

print("\nDifference between final mean and median =", abs(mean2 - median2))

expected_poisson_std = np.sqrt(10000.0)
print("Expected Poisson standard deviation =", expected_poisson_std)
print("Difference from expected std =", abs(std2 - expected_poisson_std))

print("\nThis method will not always remove every bad pixel.")
print("A bad value can remain if it lies within the rejection threshold,")
print("and extreme outliers can initially inflate the measured standard")
print("deviation and therefore make the rejection interval too wide.")


# ============================================================
# Problem 3: Use sigrej() on the original 400-element data set
# ============================================================

print("\nProblem 3")

clean_mask = sigrej(sample, (5.0, 5.0))
cleaned_data = sample[clean_mask]

print("Mean of data cleaned by sigrej() =", np.mean(cleaned_data))
print("Median of data cleaned by sigrej() =", np.median(cleaned_data))
print("Standard deviation of cleaned data =", np.std(cleaned_data))
print("Number of retained points =", cleaned_data.size)

print("\nMean from Problem 2 =", mean2)
print("Mean from sigrej()  =", np.mean(cleaned_data))
print("Difference =", abs(mean2 - np.mean(cleaned_data)))
