"""
Approach to the thin-wall limit for d=2,3,...,7.

Comparison to thin-wall results from Konoplich Theor. Math. Phys. 73 (1987)
1286-1295 and Ivanov et al. JHEP 03 (2022) 209, arXiv:2202.04498.
See also Phys.Rev.D 69 (2004) 025009, arXiv:hep-th/030720 and
Phys.Rev.D 72 (2005) 125004, arXiv:hep-th/0511156, plus new results computed
for the BubbleDet paper.
"""
import numpy as np # arrays and maths
import matplotlib.pyplot as plt # plotting
from scipy import special # gamma function
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant


# the dimension, dim = 2, 3, ... 7
dim = 4
print(f"{dim=}")


# Ivanov et al's potential (and Kosowsky et al's), with lambda and v scaled out
def V(phi, Delta):
    return 0.125 * (phi ** 2 - 1) ** 2 + Delta * (phi - 1)


# first derivative of potential
def dV(phi, Delta):
    return 0.5 * phi * (phi ** 2 - 1) + Delta


# second derivative of potential
def ddV(phi, Delta):
    return 0.5 * (3 * phi ** 2 - 1)


# metastable minimum of potential
def phi_true(Delta):
    if Delta > 0:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[0]
    else:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[-1]


# stable minimum of potential
def phi_false(Delta):
    if Delta > 0:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[-1]
    else:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[0]


# radius of thin-wall bubble
def thinwall_radius(Delta, dim):
    return (dim - 1) / (3 * Delta) + Delta * (
        6 * np.pi ** 2 - 40 + dim * (26 - 4 * dim - 3 * np.pi ** 2)
    ) / (3 * (dim - 1))


def solid_angles(dim):
    return 2 * np.pi ** (dim / 2) / special.gamma(dim / 2)


def thinwall_action_LO(Delta, dim):
    # at leading order
    return Delta ** (1 - dim) * solid_angles(dim) * (
        ((dim - 1) / 3) ** (dim - 1) * 2 / 3 / dim
    )


def thinwall_action(Delta, dim):
    # at next-to-leading order
    factor_NLO = (1 + dim * (25 - 8 * dim - 3 * np.pi ** 2)) / 2 / (dim - 1)
    return thinwall_action_LO(Delta, dim) * (1 + Delta ** 2 * factor_NLO)


# minus the logarithm of the one-loop determinant in thin-wall regime
def thinwall_log_det(Delta, dim):
    log_prefactor = (dim / 2) * (
        1 - dim + np.log(12 * thinwall_action(Delta, dim) / (2 * np.pi))
    )
    expo = Delta ** (1 - dim)
    if dim == 2:
        expo *= -1 + np.pi / 6 / np.sqrt(3)
        log_prefactor = np.log(Delta / np.pi)
    elif dim == 3:
        expo *= 10 / 27 + np.log(3) / 6
    elif dim == 4:
        expo *= 9 / 32 - np.pi / 16 / np.sqrt(3)
    elif dim == 5:
        expo *= -296 / 3645 - 2 * np.log(3) / 27
    elif dim == 6:
        expo *= -1376251 / 11197440 + 625 * np.pi / 20736 / np.sqrt(3)
    elif dim == 7:
        expo *= -1 / 140 + 3 * np.log(3) / 80
    else:
        print(f"thinwall_log_det error: dimension {dim=}")
        return float("nan")
    return expo - log_prefactor


if dim == 2:
    Deltas = np.array([0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015, 0.01])
elif dim == 3:
    Deltas = np.array([0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02])
elif dim == 4:
    Deltas = np.array(
        [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015]
    )
elif dim == 5:
    Deltas = np.array(
        [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015]
    )
elif dim == 6:
    Deltas = Deltas = np.array(
        [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015]
    )
elif dim == 7:
    Deltas = np.array([0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04])
else:
    raise ValueError(f"Error, results not known for {dim=}")
diffS = []
diffDet = []

print(
    "%-8s %-16s %-16s %-16s %-16s %-16s"
    % ("Delta", "S1", "err(S1)", "S1*Delta^(d-1)", "diff(S1)/|S1|", "err(S1)/|S1|")
)
for Delta in Deltas:
    # CosmoTransitions object
    ct_obj = SingleFieldInstanton(
        phi_true(Delta),
        phi_false(Delta),
        lambda phi: V(phi, Delta),
        lambda phi: dV(phi, Delta),
        d2V=lambda phi: ddV(phi, Delta),
        alpha=(dim - 1),
    )

    # bounce calculation
    profile = ct_obj.findProfile(
        phitol=1e-12, xtol=1e-12, npoints=4000
    )

    # bounce action

    # creating bubble config instance
    bub_config = BubbleConfig.fromCosmoTransitions(ct_obj, profile)

    # creating particle instance
    higgs = ParticleConfig(
        W_Phi=lambda phi: ddV(phi, Delta),
        spin=0,
        dof_internal=1,
        zero_modes="Higgs",
    )


    # creating bubble determinant instance
    bub_det = BubbleDeterminant(bub_config, [higgs])

    # fluctuation determinant
    S1, S1_err = bub_det.findDeterminant()

    # difference to analytic thin-wall result
    diffS1 = abs(S1 - thinwall_log_det(Delta, dim))

    diffDet.append(diffS1 / abs(S1))

    print(
        "%-8.4g %-16.8g %-16.8g %-16.8g %-16.8g %-16.8g"
        % (
            Delta,
            S1,
            S1_err,
            S1 * Delta ** (dim - 1),
            diffS1 / abs(S1),
            S1_err / abs(S1),
        )
    )


DeltasS1 = Deltas ** 2
plt.plot(DeltasS1, diffDet, "o", fillstyle="none")
plt.plot([0, DeltasS1[-1]], [0, diffDet[-1]])
plt.plot([0, DeltasS1[0]], [0, diffDet[0]])
plt.ylabel("$S_1$ relative difference")
plt.xlabel(r"$\Delta^2$")
plt.title(f"${dim=}$")
plt.show()
