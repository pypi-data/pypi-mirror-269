"""
Convergence of the WKB approximation for large orbital quantum number.

The WKB approximation reproduces the correct behaviour for the functional
determinant at large orbital quantum number. We show how the WKB approximation
converges, and how higher orders in the WKB approximation speed up the rate of
convergence.
"""
import numpy as np  # arrays and maths
import matplotlib.pyplot as plt # plotting
from scipy.optimize import curve_fit # fitting curve to results
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant


# for fits
def linear(x, a, b):
    return a + b * x


# parameters
dim = 4
msq = 1
g = -3
lam = 3 * 0.5

# potential and its derivatives
def V(x):
    return 1 / 2 * msq * x**2 + 1 / 6 * g * x**3 + lam / 24 * x**4


def dV(x):
    return msq * x + 1 / 2 * g * x**2 + lam / 6 * x**3


def ddV(x):
    return msq + g * x + lam / 2 * x**2


# minima
phi_true = (-3 * g + np.sqrt(9 * g**2 - 24 * msq * lam)) / 2 / lam
phi_false = 0

# nucleation object
ct_obj = SingleFieldInstanton(
    phi_true,
    phi_false,
    V,
    dV,
    d2V=ddV,
    alpha=(dim - 1),
)

# bounce calculation
profile = ct_obj.findProfile(
    xtol=1e-13,
    phitol=1e-13,
    npoints=4000,
    rmin=1e-5,
    rmax=1e5,
)

# creating bubble config instance
bub_config = BubbleConfig.fromCosmoTransitions(ct_obj, profile)

# creating particle instance
higgs = ParticleConfig(
    W_Phi=ddV,
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)

# creating bubble determinant instance
bub_det = BubbleDeterminant(bub_config, higgs, thermal=True)

# getting WKB results
l_min = 2
l_max = 40
l_list = np.arange(l_min, l_max)

lnTl_WKB, lnTl_WKB3, lnTl_WKB5, lnTl_WKB7, lnTl_WKB9 = bub_det.findWKB(
    higgs,
    l_max,
    separate_orders=True,
)
diff = np.zeros(l_max - 2)
diff_NLO3 = np.zeros(l_max - 2)
diff_NLO5 = np.zeros(l_max - 2)
diff_NLO7 = np.zeros(l_max - 2)
diff_NLO9 = np.zeros(l_max - 2)
# running over l
print(
    "%-8s %-16s %-16s %-16s %-16s %-16s %-16s"
    % (
        "l",
        "lnTl",
        "diff_WKB_LO",
        "diff_WKB_NLO",
        "diff_WKB_N2LO",
        "diff_WKB_N3LO",
        "diff_WKB_N4LO",
    )
)
for l in l_list:
    Tl, Tl_err, dTl = bub_det.findGelfandYaglomTl(higgs, l)
    lnTl = np.log(Tl)
    lnTl_err = Tl_err / abs(Tl)
    diff[l - l_min] = abs(lnTl - lnTl_WKB[l]) / abs(lnTl)
    diff_NLO3[l - l_min] = abs(lnTl - lnTl_WKB[l] - lnTl_WKB3[l]) / abs(lnTl)
    diff_NLO5[l - l_min] = abs(
        lnTl - lnTl_WKB[l] - lnTl_WKB3[l] - lnTl_WKB5[l]
    ) / abs(lnTl)
    diff_NLO7[l - l_min] = abs(
        lnTl - lnTl_WKB[l] - lnTl_WKB3[l] - lnTl_WKB5[l] - lnTl_WKB7[l]
    ) / abs(lnTl)
    diff_NLO9[l - l_min] = abs(
        lnTl
        - lnTl_WKB[l]
        - lnTl_WKB3[l]
        - lnTl_WKB5[l]
        - lnTl_WKB7[l]
        - lnTl_WKB9[l]
    ) / abs(lnTl)
    print(
        "%-8d %-16.8g %-16.8g %-16.8g %-16.8g %-16.8g %-16.8g"
        % (
            l,
            lnTl,
            diff[l - l_min],
            diff_NLO3[l - l_min],
            diff_NLO5[l - l_min],
            diff_NLO7[l - l_min],
            diff_NLO9[l - l_min],
        )
    )

# plotting
plt.plot(l_list, diff, "bo", fillstyle="none", label=r"WKB $l^{-1}$")
plt.plot(l_list, diff_NLO3, "ro", fillstyle="none", label=r"WKB $l^{-3}$")
plt.plot(l_list, diff_NLO5, "ko", fillstyle="none", label=r"WKB $l^{-5}$")
plt.plot(l_list, diff_NLO7, "mo", fillstyle="none", label=r"WKB $l^{-7}$")
plt.plot(l_list, diff_NLO9, "yo", fillstyle="none", label=r"WKB $l^{-9}$")

# fitting
l_min_fit = 6
l_max_fit = 25
l_fit = l_list[l_min_fit:l_max_fit]
log_l_fit = np.log(l_fit)
#
popt, pcov = curve_fit(
    linear, log_l_fit, np.log(diff[l_min_fit:l_max_fit])
)
fit_curve = np.exp(linear(log_l_fit, *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(l_fit, fit_curve, "b-", label=fit_label)

#
popt, pcov = curve_fit(
    linear, log_l_fit, np.log(diff_NLO3[l_min_fit:l_max_fit])
)
fit_curve = np.exp(linear(log_l_fit, *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(l_fit, fit_curve, "r-", label=fit_label)

#
popt, pcov = curve_fit(
    linear, log_l_fit, np.log(diff_NLO5[l_min_fit:l_max_fit])
)
fit_curve = np.exp(linear(log_l_fit, *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(l_fit, fit_curve, "k-", label=fit_label)

#
popt, pcov = curve_fit(
    linear, log_l_fit, np.log(diff_NLO7[l_min_fit:l_max_fit])
)
fit_curve = np.exp(linear(log_l_fit, *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(l_fit, fit_curve, "m-", label=fit_label)

#
popt, pcov = curve_fit(
    linear, log_l_fit, np.log(diff_NLO9[l_min_fit:l_max_fit])
)
fit_curve = np.exp(linear(log_l_fit, *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(l_fit, fit_curve, "y-", label=fit_label)



plt.ylabel(r"$\log T_l$ relative difference")
plt.xlabel(r"$l$")
plt.xscale("log")
plt.yscale("log")
plt.title("dim = " + str(dim))
plt.legend(loc="best")
plt.tight_layout()
plt.show()
