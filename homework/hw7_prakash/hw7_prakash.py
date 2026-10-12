# Rishant Prakash
# AST 5765: Advanced Astronomical Data Analysis
# Homework 7: Fitting Data and Scientific Data Presentation
# October 2026

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2


# Input parameters


datafile = "hw7_synthetic_transit_lightcurve.csv"

stellar_radius = 1.14       # solar radii
stellar_radius_err = 0.01   # solar radii

# Problem 3c tells us to adopt this uncertainty for the
# fractional transit depth regardless of the fit covariance.
depth_err = 0.002


# Problem 3a: Read and plot the observations


print("Problem 3a")

data = np.loadtxt(
    datafile,
    delimiter=",",
    skiprows=1
)

time = data[:, 0]
flux = data[:, 1]

print("Number of observations =", len(time))
print("Minimum time =", np.min(time))
print("Maximum time =", np.max(time))

plt.figure(figsize=(8, 5))

plt.scatter(
    time,
    flux,
    s=15
)

plt.xlabel("Time from transit center (days)")
plt.ylabel("Normalized Flux")
plt.title("Synthetic Exoplanet Transit Light Curve")

plt.tight_layout()

plt.savefig(
    "hw7_prakash_problem3a_transit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Problem 3b(i): Rectangular transit-window function


def box_window(x, center, width, height):
    """Return a normalized rectangular transit model.

    Parameters
    ----------
    x : array_like
        Observational times.
    center : float
        Center of the transit window.
    width : float
        Full width of the transit window.
    height : float
        Fractional transit depth.

    Returns
    -------
    model : ndarray
        Normalized flux equal to 1 outside transit and
        1 - height inside transit.
    """

    inside_transit = np.abs(x - center) <= width / 2.0

    return np.where(
        inside_transit,
        1.0 - height,
        1.0
    )


# Problem 3b(ii): Fit the transit


print("\nProblem 3b")

# Initial estimates are obtained by inspecting the light curve.
initial_guess = [
    0.0,    # center, days
    0.02,   # width, days
    0.01    # fractional depth
]

parameter_bounds = (
    [-0.05, 0.001, 0.0],
    [ 0.05, 0.100, 0.1]
)

best_parameters, covariance = curve_fit(
    box_window,
    time,
    flux,
    p0=initial_guess,
    bounds=parameter_bounds,
    maxfev=20000
)

center, width, depth = best_parameters

best_model = box_window(
    time,
    center,
    width,
    depth
)

print("Best-fit center =", center, "days")
print("Best-fit width =", width, "days")
print("Best-fit transit depth =", depth)


# Check goodness of fit


outside_transit = (
    np.abs(time - center) > width / 2.0
)

# Estimate the observational scatter from the out-of-transit data.
flux_sigma = np.std(
    flux[outside_transit],
    ddof=1
)

chisq = np.sum(
    ((flux - best_model) / flux_sigma) ** 2
)

degrees_freedom = len(flux) - len(best_parameters)

reduced_chisq = chisq / degrees_freedom

fit_probability = chi2.sf(
    chisq,
    degrees_freedom
)

print("Estimated flux uncertainty =", flux_sigma)
print("Chi-square =", chisq)
print("Degrees of freedom =", degrees_freedom)
print("Reduced chi-square =", reduced_chisq)
print("Probability of a worse chi-square =", fit_probability)

print(
    "The reduced chi-square is close to 1, so the simple box "
    "model is consistent with the scatter in this synthetic dataset."
)

print(
    "If the fit were poor, I would inspect the residuals and use "
    "a more realistic transit model including ingress, egress, "
    "and limb darkening and/or improve the uncertainty model."
)


# Problem 3b(iii): Planet radius


planet_radius = (
    stellar_radius * np.sqrt(depth)
)

print("\nProblem 3b(iii)")
print("Stellar radius =", stellar_radius, "R_sun")
print("Fractional transit depth =", depth)
print("Planet radius =", planet_radius, "R_sun")



# Problem 3b(iv): Publication-ready fit plot

model_time = np.linspace(
    np.min(time),
    np.max(time),
    2000
)

model_flux = box_window(
    model_time,
    center,
    width,
    depth
)

plt.figure(figsize=(8, 5))

plt.scatter(
    time,
    flux,
    s=15,
    label="Observations"
)

plt.plot(
    model_time,
    model_flux,
    linewidth=2,
    label="Best-fit box model"
)

plt.xlabel("Time from transit center (days)")
plt.ylabel("Normalized Flux")
plt.title("Synthetic Transit Light Curve and Best-Fit Model")

plt.legend()
plt.tight_layout()

plt.savefig(
    "hw7_prakash_problem3b_fit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()



# Problem 3c: Propagate uncertainty in planet radius


print("\nProblem 3c")

# Rp = Rstar * sqrt(depth)
#
# Error propagation:
#
# sigma_Rp^2 =
# (dRp/dRstar * sigma_Rstar)^2 +
# (dRp/ddepth * sigma_depth)^2
#
# where
# dRp/dRstar = sqrt(depth)
# dRp/ddepth = Rstar / (2 * sqrt(depth))

planet_radius_err = np.sqrt(
    (np.sqrt(depth) * stellar_radius_err) ** 2
    +
    (
        stellar_radius
        / (2.0 * np.sqrt(depth))
        * depth_err
    ) ** 2
)

print(
    "Planet radius =",
    planet_radius,
    "+/-",
    planet_radius_err,
    "R_sun"
)