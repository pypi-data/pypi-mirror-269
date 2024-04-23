# tools for extrapolation
import numpy as np  # arrays and maths
from math import fsum # reducing floating point errors in sums
import warnings # for runtime warnings
from scipy.special import gamma # to try to help with cancellations
from scipy.optimize import curve_fit # for fitting


def richardson_extrapolation(a_n, order_max=6):
    r"""Performs Richardson extrapolation

    This function performs Richardson extrapolation to accelerate the
    convergence of a series, with coefficients :math:`a_n`. Our implementation
    follows Section 8.1 of Bender and Orszag's book [BO]_. Given the partial sums
    :math:`A_n=\sum_{k=0}^{n-1}a_k`, the order :math:`N` Richardson
    extrapolation :math:`R_N` takes the form

    .. math::
      R_N = \sum_{k=0}^{N} \frac{A_{n+k} (n+k)^N (-1)^{k+N}}{k! (N-k)!}.

    This function automatically picks the order for Richardson extrapolation,
    up to order_max, so as to minimise both errors from higher order terms,
    and from floating point arithmetic.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    order_max : int, optional
        Maximum order of extrapolation, greater than or equal to 0.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The estimated error in the result.

    References
    ----------
    .. [BO] Bender, C. M., Orszag, S., and Orszag, S. A. (1999). Advanced
            mathematical methods for scientists and engineers I: Asymptotic
            methods and perturbation theory (Vol. 1). Springer Science &
            Business Media.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import richardson_extrapolation
    >>> a_n = np.array([1 / (n + 1) ** 2 for n in range(10)])
    >>> res, err = richardson_extrapolation(a_n)
    (1.6449259364244426, 1.9065728906753066e-05)
    >>> np.pi ** 2 / 6
    1.6449340668482264
    """
    # same as np.sum(a_n) at order 0
    a_n = np.trim_zeros(a_n, "b")
    res_0, err_0, err_n_0 = richardson_extrapolation_static(a_n, 0)
    res, err, err_n = richardson_extrapolation_static(a_n, 1)
    if abs(res - res_0) < err:
        return res_0, max(err_0, err_n_0)
    r = 2
    while r <= order_max:
        res_r, err_r, err_n_r = richardson_extrapolation_static(a_n, r)
        r += 1
        if err_r < abs(res - res_0) / 5 and abs(res_r - res) < abs(res - res_0):
            res_0, err_0 = res, err
            res, err, err_n = res_r, err_r, err_n_r
        else:
            break
    return res, max(err, err_n_r, abs(res - res_0))


def richardson_extrapolation_static(a_n, order):
    r"""Performs Richardson extrapolation to fixed order

    For more details see :func:`richardson_extrapolation`.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    order : int
        Order of extrapolation, greater than or equal to 0.

    Returns
    -------
    res : float
        The result of extrapolation.
    err_float : float
        The estimated error from floating point arithmetic.
    err_n : float
        The estimated error from missing higher order terms.

    Notes
    -----
    At high orders, large cancellations occur, so floating point precision
    may not be enough. Recommend keeping order less than about 6.

    """
    n_max = len(a_n)
    n_min = n_max - order - 1
    if n_min < 0:
        warnings.warn(f"{order=} too high", RuntimeWarning)
        return np.sum(a_n), float('nan'), float('nan')
    # constructing partial sums
    A_n = np.zeros(order + 1)
    for i in range(n_min + 1):
        A_n[0] += a_n[i]
    for k in range(1, order + 1):
        A_n[k] = A_n[k - 1] + a_n[n_min + k]
    # doing extrapolation
    res = 0.0
    max_factor = 1
    for k in range(order + 1):
        factor = (
            np.power(-1, (order + k) % 2)
            * np.power(n_min + k, order)
            / gamma(k + 1)
            / gamma(order - k + 1)
        )
        max_factor = max(max_factor, abs(factor))
        res += factor * A_n[k]
    # floating point error estimate
    err_float = max_factor * (order + 1) * abs(res) / 1e16
    # error estimate from missing higher-order terms
    err_n = abs(res) / np.power(n_max, order + 1)
    return res, err_float, err_n


def partial_sums(a_n):
    r"""Constructs all partial sums

    Given series coefficients :math:`a_n`, computes

    .. math::
      A_n = \sum_{j=0}^{n-1} a_j.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.

    Returns
    -------
    A_n : array

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import partial_sums
    >>> a_n = np.array([1 / 2 ** (n + 1) for n in range(5)])
    [0.5, 0.25, 0.125, 0.0625, 0.03125]
    >>> A_n = partial_sums(a_n)
    [0.5, 0.75, 0.875, 0.9375, 0.96875]
    """
    n = len(a_n)
    A_n = np.zeros(n)
    A_n[0] = a_n[0]
    for k in range(1, n):
        A_n[k] = fsum(a_n[:(k + 1)]) # A_n[k - 1] + a_n[k]
    return A_n


def fit_extrapolation(a_n, x=None, sigma=None, drop_orders=0):
    r"""Performs extrapolation based on polynomial fitting

    For a series with index :math:`n`, the function fits a polynomial
    :math:`p` in :math:`1/(n+1)` to the partial sums
    :math:`A_n=\sum_{k=0}^{n-1}a_k`,

    .. math::
      p = \sum_{k=0}^{N} \frac{c_k}{(n+1)^k},

    where here the order of the polynomial is :math:`N`. After fitting, the
    extrapolation to :math:`n\to \infty` is given by :math:`c_0`.

    This function automatically picks the polynomial order for the fit, to
    ensure a good fit without overfitting. To do so, it minimises the
    :math:`\chi^2` per degree of freedom in the fit.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    x : array_like, optional
        The independent variable, taken to be :math:`1/(n+1)` if None.
    drop_orders: int, optional
        Powers of :math:`1/n` to drop.
    sigma : array_like
        Errors on a_n, default is None.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The fit error in the result, estimated from either the square root of
        the diagonal element of the covariance matrix, or the difference
        between fits of different orders, whichever is larger.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import fit_extrapolation
    >>> a_n = np.array([1 / (n + 1) ** 2 for n in range(10)])
    >>> res, err = fit_extrapolation(a_n)
    (1.6449345845688652, 6.277329652778687e-08)
    >>> np.pi ** 2 / 6
    1.6449340668482264
    """
    n = len(a_n)
    a_n = np.trim_zeros(a_n, "b")
    A_n = partial_sums(a_n)
    if x is None:
        inv_n = 1 / (1 + np.arange(len(a_n)))
    else:
        inv_n = x
    if sigma is not None:
        err_n = np.sqrt(partial_sums(sigma ** 2))
    else:
        err_n = None
    inv_n = np.array([1 / (i + 1) for i in range(len(A_n))])
    fit, cov, diff_0, order_best, chi_sq_reduced_best = best_poly_fit(
        inv_n, A_n, drop_orders=drop_orders, sigma=err_n,
    )
    if sigma is None:
        return fit[0], diff_0
    else:
        return fit[0], max(np.sqrt(cov[0, 0]), diff_0)


def best_poly_fit(x, y, sigma=None, order_min=0, order_max=6, drop_orders=0):
    r"""Finds polynomial fit with smallest :math:`\chi^2/\text{dof}`

    Performs all possible polynomial fits in the range [order_min, order_max],
    and choses that with smallest :math:`\chi^2/\text{dof}`.

    Uses scipy.optimize.curve_fit to perform the fitting.

    Parameters
    ----------
    x : array_like
    y : array_like
    sigma : array_like

    Returns
    -------
    fit : array
        The fit parameters.
    cov : 2D array
        The covariance matrix.
    diff_0 : float
        An estimate of the difference between fits for the constant term.
    order_best: int
        The optimal polynomial order.
    chi_sq_reduced_best: float
        The value of :math:`\chi^2/\text{dof}` for the optimal fit.
    """
    # checking that dof >= 1
    n = len(x)
    o_min = min(order_min, order_max)
    o_max = max(order_min, order_max)
    o_max = max(min(o_max, n - 2), 0)
    o_min = min(max(0, o_min), o_max)
    # errors
    if sigma is None:
        sigma = np.ones(n)
    # fitting a constant first
    order_best = o_min
    fit_fn = lambda x, *coeffs:  poly_fn(x, *coeffs, drop_orders=drop_orders)
    p0 = np.ones(order_best + 1)
    fit, cov = curve_fit(fit_fn, x, y, p0=p0, sigma=sigma, absolute_sigma=True)
    diff_0 = abs(fit[0])
    diff_0_crude = True
    # goodness of fit
    dof = n - (order_best + 1)
    chi_sq = np.sum((y - poly_fn(x, *fit, drop_orders=drop_orders)) ** 2)
    chi_sq_reduced_best = chi_sq / dof
    # comparing to higher order polynomials
    for order in range(1, o_max + 1):
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            # treating warnings as errors, to break sum if raised
            try:
                fit_fn = lambda x, *coeffs: \
                    poly_fn(x, *coeffs, drop_orders=drop_orders)
                p0 = np.ones(order + 1)
                popt, pcov = curve_fit(
                    fit_fn, x, y, p0=p0, sigma=sigma, absolute_sigma=True
                )
                # goodness of fit
                n = len(x)
                dof = n - (order + 1)
                chi_sq = np.sum(
                    (y - poly_fn(x, *popt, drop_orders=drop_orders)) ** 2
                )
                chi_sq_reduced = chi_sq / dof
                if chi_sq_reduced < chi_sq_reduced_best:
                    chi_sq_reduced_best = chi_sq_reduced
                    order_best = order
                    order_min = min(order, len(fit))
                    if diff_0_crude:
                        diff_0 = abs(fit[0] - popt[0])
                    else:
                        # to avoid underestimating errors due to cancellations
                        diff_0 = np.sqrt(diff_0 * abs(fit[0] - popt[0]))
                    diff_0_crude = False
                    fit, cov = popt, pcov
            except:
                break
    return fit, cov, diff_0, order_best, chi_sq_reduced_best


def poly_fn(x, *coeffs, drop_orders=0):
    r"""Polynomial function from coefficients.

    A general polynomial function, of the appropriate form for
    scipy.optimize.curve_fit, with coefficients as parameters.

    A simple wrapper for the numpy polynomial implementation.
    Includes functionality to set some monomials to zero.

    Parameters
    ----------
    x : float
    *coeffs : floats

    Returns
    -------
    p(x) : float
        The polynomial function evaluated at x.
    """
    n_shifted_coeffs = len(coeffs) + drop_orders
    shifted_coeffs = np.zeros(n_shifted_coeffs)
    shifted_coeffs[0] = coeffs[0]
    for i in range(1, len(coeffs)):
        shifted_coeffs[drop_orders + i] = coeffs[i]
    p = np.polynomial.polynomial.Polynomial(shifted_coeffs)
    return p(x)


def shanks_extrapolation(a_n, order=6, truncate=True):
    r"""Performs iterated Shanks extrapolation

    This function performs an iterated Shanks transform, to accelerate the
    convergence of a series, with coefficients :math:`a_n`. Our implementation
    follows Section 8.1 of Bender and Orszag's book [BO]_. Given the partial
    sums :math:`A_n=\sum_{k=0}^{n-1}a_k`, a single Shanks transform takes the
    form

    .. math::
      S(A_n) = \frac{A_{n+1}A_{n-1} - A_n^2}{A_{n+1} + A_{n-1} - 2A_n}.

    This operation can be iterated to further accelerate convergence. However,
    at high orders, large cancellations occur, and with standard Python floating
    point precision the best relative accuracy which can be achieved by
    iteration is about 1e-8.

    The return value of this function is the last element of
    :math:`S^\text{order}(A_n)`.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    order: int, optional
        Number of iterations.
    truncate : boole, optional
        If True, truncates algorithm where floating point errors become
        important.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The estimated error from floating point artithmetic.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import shanks_extrapolation
    >>> a_n = np.array([1 / (n + 1) ** 2 for n in range(10)])
    >>> res, err = shanks_extrapolation(a_n)
    (1.6357502037479885, 0.0008240093298663709)
    >>> np.pi ** 2 / 6
    1.6449340668482264
    """
    a_n = np.trim_zeros(a_n, "b")
    n = len(a_n)
    order_max = min(order, (n - 1) // 2)
    SA_n = partial_sums(a_n)
    res = SA_n[-1]
    err = max(abs(res - SA_n[n // 2]), abs(a_n[-1]))
    for s in range(order_max):
        # floating point error estimate
        denom = SA_n[-1] + SA_n[-3] - 2 * SA_n[-2]
        if truncate and abs(denom) < 1e-8 * abs(SA_n[-1]):
            #warnings.warn(f"Shanks stopping at {s=}", RuntimeWarning)
            break
        # transform
        SA_n = shanks_static(SA_n)
        err_float = 1e-8 * abs(SA_n[-1])
        err = np.sqrt(err * abs(res - SA_n[-1]))
        err = max(err, err_float)
        res = SA_n[-1]
    return res, err


def shanks_static(A_n):
    r"""Performs single Shanks trasform.

    For more details see :func:`shanks_extrapolation`, which iterates this
    function.

    Parameters
    ----------
    A_n : array_like
        Series partial sums.

    Returns
    -------
    res : array
        The result of a Shanks transform. The array is shorter than A_n by 2.

    """
    SA_n = np.zeros(len(A_n) - 2)
    for n in range(len(A_n) - 2):
        n_An = n + 1
        SA_n[n] = (A_n[n_An + 1] * A_n[n_An - 1] - A_n[n_An] ** 2) / (
            A_n[n_An + 1] + A_n[n_An - 1] - 2 * A_n[n_An]
        )
    return SA_n


def epsilon_extrapolation(a_n, truncate=True, sigma=None):
    r"""Performs extrapolation using the epsilon algorithm

    The epsilon algorithm is closely related to the iterated Shanks algorithm,
    but has some superior properties for floating point numbers. In particular,
    its relative accuracy is not bounded by the square root of the floating
    point error, but can exaust the accuracy of floating point numbers. For an
    overview of the epsilon algorithm, see [GM]_.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    truncate : boole, optional
        If True, truncates algorithm where cancellation errors start to become
        large.
    sigma : array_like, optional
        Error estimates for a_n.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The estimated error in the extrapolation.

    References
    ----------
    .. [GM] Graves-Morris, P.R., Roberts, D.E. and Salam, A., 2000. The epsilon
            algorithm and related topics. Journal of Computational and Applied
            Mathematics, 122(1-2), pp.51-80.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import epsilon_extrapolation
    >>> a_n = np.array([(-1) ** n / (n+1) for n in range(10)])
    >>> res, err = epsilon_extrapolation(a_n)
    (0.6931471424877166, 1.898666642796698e-07)
    >>> np.log(2)
    0.6931471805599453
    """
    MAX_RATIO = 3 # a metaparameter determining when errors are too large
    a_n = np.trim_zeros(a_n, "b")
    n = len(a_n)
    A_n = partial_sums(a_n)
    # initialising epsilon_-1 and epsilon_0
    epsilon_previous = np.zeros(n)
    epsilon_current = A_n
    # best current result, and error estimate
    res = A_n[-1]
    err = max(abs(res - A_n[n // 2]), abs(a_n[-1]))
    # k_max largest odd number <=n
    k_max = n if n % 2 == 1 else n - 1
    for k in range(1, k_max):
        epsilon_next = np.zeros(n - k)
        for j in range(n - k):
            epsilon_diff = epsilon_current[j + 1] - epsilon_current[j]
            # testing for 1 / 0
            if epsilon_diff == 0:
                #print(f"Encountered 1/0 at {k=}")
                return res, err
            # testing for large cancellations
            epsilon_max_abs = max(
                abs(epsilon_current[j + 1]),
                abs(epsilon_current[j]),
            )
            float_err = 2e-16 * abs(res) * (
                0.5 * abs(epsilon_max_abs) / abs(epsilon_diff)
            )
            if sigma is not None:
                err_j = max(float_err, sigma[j])
            else:
                err_j = float_err
            if truncate and res != 0 and err_j > err:
                #print(f"Error too large at {k=}")
                return res, err
            # non-trivial part of algorithm
            epsilon_next[j] = epsilon_previous[j + 1] + 1 / epsilon_diff
        # storing 3 epsilons at a time
        epsilon_previous = epsilon_current
        epsilon_current = epsilon_next
        # best current result, and error estimate
        if k % 2 == 0:
            err_new = abs(epsilon_current[-1] - res)
            if err_new == 0:
                #print(f"Zero error at {k=}")
                break
            elif err_new > MAX_RATIO * err: # error growing (too much)
                #print(f"Error growing at {k=}")
                break
            err = np.sqrt(err * err_new)
            res = epsilon_current[-1]
    return res, err
