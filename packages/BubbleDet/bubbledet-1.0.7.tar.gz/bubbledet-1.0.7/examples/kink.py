"""
One-loop correction to the split between energy eigenvalues, in d=1.

We compare to the analytic results in Sidney Coleman's Uses of Instantons,
Appendix B, for the symmetry-breaking phi**4 potential and the sine-Gordon
potential.
"""
import numpy as np
import matplotlib.pyplot as plt
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant


# coordinates for constructing our custom bounce
dim = 1
xmin = 0
xmax = 20
xkink = (xmax + xmin) / 2
npoints = 1000
dx = (xmax - xmin) / (npoints - 1)
x = np.arange(0, npoints) * dx + xmin


# phi^4 Z2 symmetry-breaking potential, in dimensionless form
def V(phi):
    return -0.5 * phi**2 + 0.25 * phi**4


def dV(phi):
    return -phi + phi**3


def ddV(phi):
    return -1 + 3 * phi**2


# the analytic kink solution
phi_meta = 1 # phi on right
m0 = np.sqrt(ddV(phi_meta))
arg = m0 / 2 * (x - xkink)
Phi = np.tanh(arg)
dPhi = m0 / 2 / np.cosh(arg) ** 2

# creating bubble config instance
bub_config = BubbleConfig(
    V=V,
    phi_metaMin=phi_meta,
    R=x,
    Phi=Phi,
    dPhi=dPhi,
    dim=1,
    dV=dV,
    d2V=ddV,
)

# creating particle instance
higgs = ParticleConfig(
    W_Phi=ddV,
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)

# computing functional determinant
bub_det = BubbleDeterminant(bub_config, higgs)
S1, S1_err = bub_det.findDeterminant()

# analytic result
S1_analytic = 1 / 2  * np.log(np.pi) - 7 / 4 * np.log(2)

# printing results
print("One-loop correction to split between energy eigenstates")
print("\nphi^4 model:")
print(
    "%-16s %-16s %-16s %-16s"
    % ("Numerical", "Error estimate", "Analytical", "Difference")
)
print(
    "%-16g %-16g %-16g %-16g"
    % (
        S1,
        S1_err,
        S1_analytic,
        abs(S1 - S1_analytic),
    )
)


# sine-Gordon potential, in dimensionless form
def V(phi):
    return 1 - np.cos(phi)


def dV(phi):
    return np.sin(phi)


def ddV(phi):
    return np.cos(phi)


# the analytic kink solution
phi_meta = 2 * np.pi # phi on right
m0 = np.sqrt(ddV(phi_meta))
arg = x - xkink
Phi = 4 * np.arctan(np.exp(arg))
dPhi = 2 / np.cosh(arg)

# creating bubble config instance
bub_config = BubbleConfig(
    V=V,
    phi_metaMin=phi_meta,
    R=x,
    Phi=Phi,
    dPhi=dPhi,
    dim=1,
    dV=dV,
    d2V=ddV,
)

# creating particle instance
higgs = ParticleConfig(
    W_Phi=ddV,
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)

# computing functional determinant
bub_det = BubbleDeterminant(bub_config, higgs)
S1, S1_err = bub_det.findDeterminant()

# exact analytic result
S1_analytic = -np.log(4 / np.sqrt(np.pi))

# printing results
print("\nSine-Gordon model:")
print(
    "%-16s %-16s %-16s %-16s"
    % ("Numerical", "Error estimate", "Analytical", "Difference")
)
print(
    "%-16g %-16g %-16g %-16g"
    % (
        S1,
        S1_err,
        S1_analytic,
        abs(S1 - S1_analytic),
    )
)
