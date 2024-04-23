import numpy as np


def S1_scaleless(dim, Lambda, RScale, mu):
    if dim == 3:
        return dim * np.log(RScale) + np.log(Lambda) + 4.41321
    elif dim == 4:
        return (
            dim * np.log(RScale)
            + 5 / 2 * np.log(Lambda)
            + 3 * np.log(mu * RScale)
            - 0.991929
        )
    elif dim == 6:
        return (
            dim * np.log(RScale)
            + 7 * np.log(Lambda)
            - 18 / 5 * np.log(mu * RScale)
            - 16.1573
        )
    else:
        raise ValueError("{dim=} not in [3, 4, 6]")
