"""
Demonstrating extralation methods
"""
import numpy as np  # arrays and maths
import matplotlib.pyplot as plt  #  plotting
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant
from BubbleDet.extrapolation import (
    partial_sums,
    epsilon_extrapolation,
    fit_extrapolation,
)

# dimension
dim = 6

# parameters
msq = 0.2
g = -1
lam = 1


# potential and its derivatives
def V(x):
    return 1 / 2 * msq * x**2 + 1 / 6 * g * x**3 + 1 / 24 * x**4


def dV(x):
    return msq * x + 1 / 2 * g * x**2 + 1 / 6 * x**3


def ddV(x):
    return msq + g * x + 1 / 2 * x**2


# minima
phi_true = (-3 * g + np.sqrt(9 * g**2 - 24 * msq)) / 2
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
profile = ct_obj.findProfile(npoints=2000, xtol=1e-12, phitol=1e-12)

# bounce action
S0 = ct_obj.findAction(profile)

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
bub_det = BubbleDeterminant(bub_config, [higgs])

# maximum l to consider
l_min = 15
l_max = 80
l_array = np.arange(l_max)
x_array = 1 / np.arange(l_min, l_max)
# x_extended = 1 / np.arange(1, l_max)


def get_epsilon(S1_array, l_min, l_max):
    S1_epsilon, err_epsilon = epsilon_extrapolation(
        S1_array[l_min : (l_max + 1)],
        truncate=True,
    )
    S1_epsilon += np.sum(S1_array[:l_min])
    return S1_epsilon, err_epsilon


def get_fit(S1_array, l_min, l_max):
    drop_orders = 8 - dim if dim < 8 else 0
    x_array = 1 / np.arange(l_min, (l_max + 1))
    S1_fit, err_fit = fit_extrapolation(
        S1_array[l_min : (l_max + 1)],
        x=x_array,
        drop_orders=drop_orders,
    )
    S1_fit += np.sum(S1_array[:l_min])
    return S1_fit, err_fit


# getting result
S1_array, err_array = bub_det.findDeterminant(l_max=l_max, full=True)
S1_array = S1_array[0]
err_array = err_array[0]
S1_partial_sums = partial_sums(S1_array)

l_plot = np.arange(l_min, l_max)
S1_epsilon_plot = []
err_epsilon_plot = []
S1_fit_plot = []
err_fit_plot = []
for l in l_plot:
    S1, err = get_epsilon(S1_array, 2, l)
    S1_epsilon_plot.append(S1)
    err_epsilon_plot.append(err)
    S1, err = get_fit(S1_array, 2, l)
    S1_fit_plot.append(S1)
    err_fit_plot.append(err)

plt.errorbar(
    x_array,
    S1_partial_sums[l_min:],
    yerr=err_array[l_min:],
    fmt="-",
    capsize=20,
    label="data",
)
plt.errorbar(
    1 / l_plot,
    S1_epsilon_plot,
    yerr=err_epsilon_plot,
    fmt="o",
    fillstyle="none",
    capsize=20,
    label="epsilon",
)
plt.errorbar(
    1 / l_plot, S1_fit_plot, yerr=err_fit_plot, fmt="+", capsize=20, label="fit"
)
plt.xlim(-1 / l_max, 1 / l_min)
plt.ylabel("$S_1$")
plt.xlabel("$1/(l+1)$")
plt.legend(loc="best")
plt.title(f"{dim=}")
plt.tight_layout()
plt.show()
