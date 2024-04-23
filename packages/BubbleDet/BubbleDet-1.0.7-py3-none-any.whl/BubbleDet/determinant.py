# import libraries
import warnings # for runtime warnings etc
import numpy as np  # arrays and maths
from scipy import special  # special functions
from cosmoTransitions.helper_functions import deriv14  # derivatives for arrays

# import local files
from .group_volumes import group_volume
from .extrapolation import (
    fit_extrapolation,
    epsilon_extrapolation,
)
from .configs import BubbleConfig, ParticleConfig, DeterminantConfig
from .phi_infinity import findLogPhiInfinity, findWInf
from .negative_eigenvalue import findNegativeEigenvalue
from .wkb import findWKB
from .gelfand_yaglom import findGelfandYaglomTl, findGelfandYaglomFl
from .renormalisation import findRenormalisationTerm
from .derivative_expansion import findDerivativeExpansion


class BubbleDeterminant:
    r"""Class for computing functional determinants.

    The main class of the BubbleDet package.

    Parameters for initialisation below.

    Parameters
    ----------
    bubble : BubbleConfig
        Object describing the background field.
    particles : list of ParticleConfig
        List of ParticleConfig objects, describing the fluctuating particles.
        Can also be a single ParticleConfig object.
    gauge_groups : list, optional
        List of length two describing the full and unbroken gauge groups,
        separated by spaces for product groups e.g. ["SU5", "SU3 SU2 U1"].
        Applies to the simple Lie groups SU(N), U(N), SO(N) and SP(N). Default
        is :py:data:`None`.
    renormalisation_scale : float, optional
        The renormalisation scale in the :math:`\text{MS}` bar scheme. If
        :py:data:`None`, set to the mass of the nucleating field.
    thermal : boole, optional
        If :py:data:`True`, includes the thermal dynamical prefactor. Default
        is :py:data:`False`.
    """
    def __init__(
        self,
        bubble,
        particles,
        gauge_groups=None,
        renormalisation_scale=None,
        thermal=False,
    ):
        # assigning member variables
        self.bubble = bubble
        try:
            self.n_particles = len(particles)
            self.particles = particles
        except:
            self.n_particles = 1
            self.particles = [particles]
        # construct determinant configs
        self.configs = []
        for particle in self.particles:
            config = DeterminantConfig(
                bubble,
                particle,
                renormalisation_scale=renormalisation_scale,
                gauge_groups=gauge_groups,
                thermal=thermal,
            )
            self.configs.append(config)

    def findDeterminant(
        self,
        eig_tol=1e-6,
        full=False,
        gy_tol=1e-6,
        l_max=None,
        log_phi_inf_tol=0.001,
        rmin=1e-4,
        tail=0.007,
    ):
        r"""Full determinant

        This function computes the determinant for the full multi-particle case.
        Mathematically, the return value is the sum of single-particle
        determinants,

        .. math::
            \texttt{findDeterminant()} =
                \sum_{\texttt{particle}}
                \texttt{findSingleDeterminant(particle)}.

        The particles summed over are those in the initialisation of the
        BubbleDeterminant object. Additional parameters and metaparameters are
        as for the single-particle case.

        Parameters
        ----------
        eig_tol : float, optional
            Relative tolerance for negative eigenvalue computation. Relevant
            to the thermal case.
        full : boole, optional
            If :py:data:`True`, returns list of single particle determinants,
            split into orbital quantum number, else returns (extrapolated) sum.
            Default is :py:data:`False`.
        gy_tol : float, optional
            Relative tolerance for solving Gelfand-Yaglom initial value
            problems.
        l_max : int, optional
            The maximum value of the orbital quantum number. If :py:data:`None`,
            then this value is estimated based on the radius of the bubble and
            the Compton wavelength of the fluctuating field.
        log_phi_inf_tol : float, optional
            An estimate of the relative uncertainty on the tail of the profile,
            for computing :math:`\log\phi_\infty`.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.
        tail : float, optional
            A parameter determining the fraction of the bubble to consider when
            fitting for the asymptotic behaviour, :math:`\log\phi_\infty`.

        Returns
        -------
        res : float
            The result of computing the full determinant.
        err : float
            Estimated error of the result.
        """
        S1_list = np.empty(self.n_particles, dtype=object)
        err_list = np.empty(self.n_particles, dtype=object)

        for i_particle in range(self.n_particles):
            particle = self.particles[i_particle]
            S1_list[i_particle], err_list[i_particle] = \
                self.findSingleDeterminant(
                    particle=particle,
                    rmin=rmin,
                    l_max=l_max,
                    tail=tail,
                    log_phi_inf_tol=log_phi_inf_tol,
                    eig_tol=eig_tol,
                    gy_tol=gy_tol,
                    full=full,
                )

        if full:
            return np.array(S1_list), np.array(err_list)
        else:
            return np.sum(S1_list), np.sum(err_list)

    def findSingleDeterminant(
        self,
        particle,
        eig_tol=1e-6,
        full=False,
        gy_tol=1e-6,
        l_max=None,
        log_phi_inf_tol=0.001,
        rmin=1e-4,
        tail=0.007,
    ):
        r"""Single particle determinant

        The functional determinant is the one-loop correction to the action
        induced by fluctuations of a field. It is also the statistical part of
        the bubble nucleation rate.

        The computation factorises based on orbital quantum number, :math:`l`.
        For each value of :math:`l`, the functional determinant is computed
        using the Gelfand-Yaglom method. This is carried out for
        :math:`l\in [0, l_\text{max}]`, and then extrapolated to
        :math:`l_\text{max} \to \infty`.

        Mathematically, the return value is

        .. math::
            \texttt{findSingleDeterminant(particle)} &= \\
                \frac{\text{dof}(d,s,n)}{2}&
                \log\frac{\det {'} (-\nabla^2 + W(r))}{\det (-\nabla^2 + W(\infty))}
                    - \log \mathcal{J} \mathcal{V},

        where the dash denotes that zero eigenvalues have been dropped from the
        first term (if present). Their effect is captured by the Jacobian
        :math:`\mathcal{J}` and volume :math:`\mathcal{V}` factors. The volume
        factor is only included for finite internal groups. The factor
        :math:`\text{dof}(d,s,n)` is the total number of internal
        and spin degrees of freedom of the field. Ultraviolet divergences are
        regulated in the :math:`\text{MS}` bar scheme.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        eig_tol : float, optional
            Relative tolerance for negative eigenvalue computation. Relevant
            to the thermal case.
        full : boole, optional
            If True, returns results split into orbital quantum number, else
            returns (extrapolated) sum. Default is False.
        gy_tol : float, optional
            Relative tolerance for solving Gelfand-Yaglom initial value
            problems.
        l_max : int, optional
            The maximum value of the orbital quantum number. If :py:data:`None`,
            then this value is estimated based on the radius of the bubble and
            the Compton wavelength of the fluctuating field.
        log_phi_inf_tol : float, optional
            An estimate of the relative uncertainty on the tail of the profile,
            for computing :math:`\log\phi_\infty`.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.
        tail : float, optional
            A parameter determining the fraction of the bubble to consider when
            fitting for the asymptotic behaviour, :math:`\log\phi_\infty`.

        Returns
        -------
        res : float
            The result of computing the single particle determinant.
        err : float
            Estimated error of the result.
        """
        # getting relevant determinant config
        config = self.__getParticleConfig(particle)
        dim = config.dim

        # extracting the asymptotic value of the field
        log_phi_inf, log_phi_inf_err = self.findLogPhiInfinity(
                log_phi_inf_tol=log_phi_inf_tol, tail=tail
        )

        if dim == 1:
            # a single functional determinant in d = 1, no sum over l
            S1_array = np.zeros(1)
            err_array = np.zeros(1)

            if config.zero_modes.lower() == "higgs":
                ddphi_0 = config.dV(config.Phi[0])
                ddphi_0_alt = deriv14(config.dPhi[:10], config.R[:10])[0]
                if ddphi_0 == 0 or ddphi_0_alt == 0:
                    # can happen if thin-wall bubble inaccurate
                    log_ddphi_0 = np.log(max(abs(ddphi_0), abs(ddphi_0_alt)))
                     # assumes due to floating point errors
                    log_ddphi_0_err = - np.log(2e-16)
                    warnings.warn("ddphi=0 at r=0", RuntimeWarning)
                else:
                    log_ddphi_0 = np.log(abs(ddphi_0))
                    log_ddphi_0_err = abs(
                        np.log(abs(ddphi_0)) - np.log(abs(ddphi_0))
                    )
                S1_array[0] = -0.5 * (
                    -0.5 * np.log(2 * np.pi)
                    + log_phi_inf
                    + np.log(abs(ddphi_0))
                )
                err_array[0] = 0.5 * (log_phi_inf_err + log_ddphi_0_err)
            elif config.zero_modes.lower() == "goldstone":
                S1_array[0] = -0.5 * (
                    - 0.5 * np.log(2 * np.pi)
                    + log_phi_inf
                    + np.log(abs(config.Phi[0]))
                )
                err_array[0] = 0.5 * log_phi_inf_err
            else:
                Tl, Tl_err = self.findGelfandYaglomTl(
                    particle,
                    1,
                    gy_tol=gy_tol,
                    rmin=rmin,
                )
                S1_array[0] = 0.5 * np.log(abs(Tl)) # modulused
                err_array[0] = 0.5 * Tl_err / abs(Tl)
        elif dim > 1:
            # functional determinants in d > 1, sum over l to infinity

            # range of l to sum over
            l_mR = self.__lMassRadius(particle)
            l_max_act = self.__chooseLmax(particle, l_max)
            S1_array = np.zeros(l_max_act)
            err_array = np.zeros(l_max_act)
            truncate = True if l_max == None else False

            if config.massless_Higgs:
                # We fit, for large R,
                # log(DW) = W_exp * log(phi) + W_pot
                W_exp, W_const = findWInf(config.Phi, config.Delta_W)

                # We can rewrite this as W~W_inf r**-a_inf
                # by using the asymptotic behaviour of phi
                coeff = special.gamma(dim / 2 - 1) * 2 ** (dim / 2 - 2)
                Delta_W_inf = W_const * np.power(coeff * np.exp(log_phi_inf), W_exp)
                a_inf = W_exp * (dim - 2)
            else:
                Delta_W_inf = None
                a_inf = None

            # constructing WKB part
            WKB, err_WKB, sum_WKB = self.findWKB(
                particle, l_max_act, Delta_W_inf=Delta_W_inf, a_inf=a_inf,
            )

            #zero modes
            if config.zero_modes.lower() == "higgs":
                # helper variables
                ddphi_0 = config.dV(config.Phi[0]) / dim
                ddphi_0_alt = deriv14(config.dPhi[:10], config.R[:10])[0]
                if ddphi_0 == 0 or ddphi_0_alt == 0:
                    # can happen if thin-wall bubble inaccurate
                    log_ddphi_0 = np.log(max(abs(ddphi_0), abs(ddphi_0_alt)))
                     # assumes due to floating point errors
                    log_ddphi_0_err = - np.log(2e-16)
                    warnings.warn("ddphi=0 at r=0", RuntimeWarning)
                else:
                    log_ddphi_0 = np.log(abs(ddphi_0))
                    log_ddphi_0_err = abs(
                        np.log(abs(ddphi_0)) - np.log(abs(ddphi_0))
                    )

                # l = 0 contribution, modulused
                if config.scaleless:
                    zero_mode_0 = (
                        (dim - 2) / 2 * config.Phi[0]
                        + config.R[0] * config.dPhi[0]
                    )
                    S1_array[0] = -(1 / 2) * (
                        (dim / 2 - 1) * np.log(2 * np.pi)
                        + log_phi_inf
                        + np.log(zero_mode_0)
                        + np.log((dim - 2) / 2)
                    )
                    err_array[0] = (1 / 2) * log_phi_inf_err
                else:
                    Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(
                        particle, 0, gy_tol=gy_tol, rmin=rmin,
                    )
                    S1_array[0] = 0.5 * np.log(abs(Tl))
                    err_array[0] = 0.5 * Tl_err / abs(Tl)

                # l = 1 contribution
                S1_array[1] = -(dim / 2) * (
                    (dim / 2 - 1) * np.log(2 * np.pi)
                    + log_phi_inf
                    + log_ddphi_0
                )
                err_array[1] = (dim / 2) * (log_phi_inf_err + log_ddphi_0_err)
            elif config.zero_modes.lower() == "goldstone":
                # l = 0 contribution
                S1_array[0] = -(1 / 2) * (
                    (dim / 2 - 1) * np.log(2 * np.pi)
                    + np.log(abs(config.Phi[0]))
                    + log_phi_inf
                )
                err_array[0] = 0.5 * log_phi_inf_err
                # l = 1 contribution
                Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(
                    particle, 1, gy_tol=gy_tol, rmin=rmin,
                )
                S1_array[1] = 0.5 * self.__degeneracy(dim, 1) * np.log(Tl)
                err_array[1] = 0.5 * self.__degeneracy(dim, 1) * Tl_err / Tl
            else: # no zero modes
                # l = 0 contribution
                Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(
                    particle, 0, gy_tol=gy_tol, rmin=rmin,
                )
                S1_array[0] = 0.5 * np.log(Tl)
                err_array[0] = 0.5 * Tl_err / Tl
                # l = 1 contribution
                Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(
                    particle, 1, gy_tol=gy_tol, rmin=rmin,
                )
                S1_array[1] = 0.5 * self.__degeneracy(dim, 1) * np.log(Tl)
                err_array[1] = 0.5 * self.__degeneracy(dim, 1) * Tl_err / Tl

            # l >= 2 contribution
            for l in range(2, l_max_act):
                deg_factor = 0.5 * self.__degeneracy(dim, l)
                with warnings.catch_warnings():
                    warnings.filterwarnings("error")
                    # treating warnings as errors, to break sum if raised
                    try:
                        if config.massless_Higgs:
                            Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(
                                particle, l, gy_tol=gy_tol, rmin=rmin,
                            )
                            Fl = np.log(self.__findGelfandYaglomAsymptotic(
                                    particle, l, Tl, Tl_D, Delta_W_inf, a_inf,
                            ))
                            Fl_err = 0
                        else:
                            Fl, Fl_err = self.findGelfandYaglomFl(
                                particle, l, gy_tol=gy_tol, rmin=rmin,
                            )

                        S1_array[l] = deg_factor * (Fl - WKB[l])
                        err_array[l] = deg_factor * Fl_err

                        # checking if can break early
                        if truncate and self.__testTruncate(
                                l, l_mR, S1_array, err_array
                            ):
                            S1_array = np.resize(S1_array, l + 1)
                            err_array = np.resize(err_array, l + 1)
                            #print(f"l_max reduced to {l}, {l_mR=}.")
                            break
                    except RuntimeWarning as ex:
                        # a warning has been raised
                        warnings.resetwarnings()
                        warnings.warn(ex)
                        warnings.warn(f"truncating sum at {l=}")
                        S1_array = np.resize(S1_array, l)
                        err_array = np.resize(err_array, l)
                        #print(f"l_max reduced to {l}, {l_mR=}.")
                        break

            # renormalisation-scale-dependent contribution
            S1_renorm, S1_renorm_eps, err_renorm = self.findRenormalisationTerm(
                particle
            )
            S1_array[0] += S1_renorm + sum_WKB
            # combining different errors simplemindedly
            err_array[0] = np.sqrt(
                err_array[0] ** 2 + err_renorm ** 2 + err_WKB ** 2
            )

            # accounting for spin degrees of freedom
            S1_array *= self.__dofSpin(particle)
            err_array *= self.__dofSpin(particle)
            if config.spin == 1:
                S1_array[0] += -2 * S1_renorm_eps

        # internal degrees of freedom
        S1_array *= config.dof_internal
        err_array *= config.dof_internal

        # volume of broken gauge group
        if (
            config.gauge_groups is not None
            and config.zero_modes.lower() == "goldstone"
        ):
            group_volume = self.__groupVolumeFactor(particle)
            S1_array[0] += -np.log(group_volume)

        # dynamical prefactor in thermal case
        if config.thermal and config.zero_modes.lower() == "higgs":
            eig_neg, eig_neg_err = self.findNegativeEigenvalue(eig_tol=eig_tol)
            S1_array[0] -= np.log(np.sqrt(abs(eig_neg)) / (2 * np.pi))
            err_array[0] += 0.5 * eig_neg_err / abs(eig_neg)

        if full:
            return S1_array, err_array
        elif dim == 1:
            return S1_array[0], err_array[0]
        else:
            # extrapolation
            # extrapolation with the epsilon algorithm
            mask = abs(S1_array) > 10 * err_array
            if sum(mask) == 0:
                mask = np.full(len(mask), True)
            S1_epsilon, err_epsilon = epsilon_extrapolation(
                S1_array[mask], sigma=err_array[mask], truncate=True,
            )
            # extrapolation by fitting a polynomial in 1 / l
            with warnings.catch_warnings():
                warnings.filterwarnings("error")
                try:
                    drop_orders = 8 - dim if dim < 8 else 0
                    S1_fit, err_fit = fit_extrapolation(
                        S1_array, drop_orders=drop_orders, sigma=err_array,
                    )
                except:
                    S1_fit = np.nan
                    err_fit = np.inf
            # choosing extrapolation result with smallest error
            if err_epsilon < err_fit:
                S1 = S1_epsilon
                err_extrap = err_epsilon
            else:
                S1 = S1_fit
                err_extrap = err_fit

            # putting errors together
            err = np.sqrt(np.sum(err_array ** 2) + err_extrap ** 2)

            # returning final result
            return S1, err


    def findGelfandYaglomTl(self, particle, l, gy_tol=1e-6, rmin=1e-4):
        r""":math:`T=\psi/\psi_{\rm FV}` for given :math:`l`

        This function solves the ode:

        .. math::
            T'' + U T' - \Delta W T = 0,

        as part of Gelfand-Yaglom method to compute functional determinants.
        Here dash denotes a derivative with respect to the radial coordinate
        :math:`r`.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l : int
            Orbital quantum number.
        gy_tol : float, optional
            Relative tolerance for solving Gelfand-Yaglom initial value
            problem.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.

        Returns
        -------
        res : float
            The result :math:`T(r_\text{max})`.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findGelfandYaglomTl(config, l, gy_tol=gy_tol, rmin=rmin)

    def findGelfandYaglomFl(self, particle, l, gy_tol=1e-6, rmin=1e-4):
        r""":math:`F=\log(\psi/\psi_{\rm FV})` for given :math:`l`

        This function solves the ode:

        .. math::
            F'' + (F')^2+U F' - \Delta W = 0,

        as part of Gelfand-Yaglom method to compute functional determinants.
        Here dash denotes a derivative with respect to the radial coordinate
        :math:`r`.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l : int
            Orbital quantum number.
        gy_tol : float, optional
            Relative tolerance for solving Gelfand-Yaglom initial value
            problem.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.

        Returns
        -------
        res : float
            The result :math:`F(r_\text{max})`.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findGelfandYaglomFl(config, l, gy_tol=gy_tol, rmin=rmin)

    def __findGelfandYaglomAsymptotic(
        self, particle, l, T0, T0D, Delta_W_inf, a_inf
    ):
        r"""Solves ode for :math:`T=\psi/\psi_{\rm FV}`

        .. math::
            T'' + U T' - W T = 0,

        as part of Gelfand-Yaglom method to compute functional determinants.
        Here dash denotes a derivative with respect to the radial coordinate
        :math:`r`. This method calculates, analytically, the solution when the
        bounce that does not vanish exponentially for large r, i.e. when the
        Higgs field is massless in the metastable phase.


        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l : int
            Orbital quantum number.
        T0: float
            the value of :math:`T_l(r_\text{max})`.
        T0D: float
            the value of :math:`\partial T_l(r_\text{max})`.
        Delta_W_inf : float
            The prefactor :math:`W_\inf` in the fit at large radii
            :math:`\Delta W \approx W_\inf r^{-a_\inf}`.
        a_inf : float
            The exponent :math:`a_\inf` in the fit at large radii
            :math:`\Delta W \approx W_\inf r^{-a_\inf}`.

        Returns
        -------
        res : float
            The result :math:`T(inf)`.

        """
        # set up
        config = self.__getParticleConfig(particle)
        d = config.dim
        rmax = config.R[-1]
        DWinf = Delta_W_inf

        alphaHelp=(2-d - 2*l )/(a_inf - 2) #order of the bessel functions
        argHelp=-2*rmax**(1 - a_inf/2.)*np.sqrt(DWinf+0j)/(-2 + a_inf) #argument of the bessel functions
        WinfHelp=(DWinf+0j)**((-2 + d + 2*l)/(2.*(-2 + a_inf))) #prefactor
        RinfHelp=rmax**((2 - d  - 2*l)/2.) #prefactor depning on rmax

        #When solve the full ODE we get two free constants that we have to fix to match the value and the derivative
        #of Tl at r=rmax

        #A1 and A2 are the functions multiplying the c1 and c2 constants
        A1=RinfHelp*WinfHelp*special.kv(alphaHelp,argHelp)
        A2=RinfHelp*WinfHelp*special.iv(-alphaHelp,argHelp)

        #B1 and B2 are the derivatives of A1 respectively A2
        B1=-(d  + 2*l - 2)/2*RinfHelp/rmax*WinfHelp*special.kv(alphaHelp,argHelp)
        B1+= -RinfHelp*WinfHelp/2*rmax**(-a_inf/2)*np.sqrt(DWinf+0j)*(special.kv(-1-alphaHelp,argHelp)+special.kv(1-alphaHelp,argHelp))
        B2=-(d  + 2*l - 2)/2*RinfHelp/rmax*WinfHelp*special.iv(-alphaHelp,argHelp)
        B2+=RinfHelp*WinfHelp/2*rmax**(-a_inf/2)*np.sqrt(DWinf+0j)*(special.iv(-1-alphaHelp,argHelp)+special.iv(1-alphaHelp,argHelp))



        #Only the c1 constant contribute to the r=inf value of Tl
        c1=-((B2*T0 - A2*T0D)/(A2*B1 - A1*B2))

        #The prefactor is the asymptotic value of A1
        Tinf=np.real(c1*((-1+0j)**((-2 + d + 2*l)/(-2 + a_inf))*(-2 + a_inf)**((-2 + d + 2*l)/(-2 + a_inf))
            *special.gamma((-2 + d + 2*l)/(-2 + a_inf)))/2.)

        if Tinf < 0:
            raise ValueError("Negative determinant. Choose a smaller lmax or provide a more accurate profile.")

        return Tinf

    def findRenormalisationTerm(self, particle):
        r""" Renormalization of divergent terms

        This routines renormalizes divergent terms and adds the appropriate
        counterterm to render the result finite.
        These terms are only nonzero in even dimensions. The present
        implementation gives the nonzero results for :math:`d = 2, 4, 6`,
        and dimensional regularization is used with :math:`d=2n-2\epsilon`.

        The divergent term can be found from the WKB approximation,
        for example for a scalar field in :math:`d = 4`

        .. math::
            -\frac{1}{2} \sum_l \deg(d;l)
                \log \frac{\psi^l_{b}(\infty)}{\psi^l_{F}(\infty)}
                \sim \frac{1}{16}\sum_l \deg(d;l)\frac{1}{ \overline{l}^3}
                \int \mathrm{d}r r^3\left[W(r)^2-W(\infty)^2\right]

        The sum over :math:`l` has an :math:`\epsilon` pole and gives a contribution

        .. math::
            \left(\frac{\exp (\gamma ) \mu ^2}{4 \pi }\right)^{\epsilon}
                \sum_{l=2}^{\infty}\deg(d;l)
                \overline{l}^{-3}
                =\frac{1}{2\epsilon} + \log\mu
                - \frac{1}{2}\left(\log 4\pi-\gamma\right)+\mathcal{O}(\epsilon)

        The counterterm contribution is

        .. math::
             S_\text{ct}[\phi] = \frac{1}{32 \epsilon}
                \int \mathrm{d}r  r^{3-2 \epsilon}
                \frac{\pi ^{-\epsilon}}{\Gamma (2-\epsilon)} W(\phi)^2.

        After adding adding the counterterm contribution to the divergent WKB
        term all :math:`\epsilon` poles cancel
        and one finds the finite result:

        .. math::
            -\frac{1}{16}\int \mathrm{d}r rr^3
                \left[W(\phi_{b}(r))^2-W(\phi_{F})^2\right]
                \left[\log \left(\frac{\mu r}{2}\right)-a-\frac{1}{2}+\gamma\right]

        The contributions are analogous in :math:`d=2` and :math:`d=6`.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the renormalisation term.

        Returns
        -------
        res : float
            The renormalisation scale dependent term.
        res_eps : float
            The additional finite renormalisation scale dependent term which
            arises due to factors of :math:`d/\epsilon` for vector fields.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findRenormalisationTerm(config)

    def findWKB(
            self,
            particle,
            l_max,
            Delta_W_inf=None,
            a_inf=None,
            separate_orders=False,
        ):
        r""" WKB approximation for large l

        Our implementation is an higher-orders generalization of [GO]_.

        The routine solves the differential equation

        .. math::
            \Psi''(x)=(x^2 W(e^x)+\overline{l}^2)\Psi(x)

        in powers of :math:`\overline{l}=l+(d-2)/2`, where :math:`r=e^x`. The
        false vacuum equation has :math:`W(\infty)` instead.
        The WKB approximation of
        :math:`\log \frac{\Psi(\infty)}{\Psi_{FV}(\infty)}`
        is then computed up to :math:`O\left(\overline{l}^{-10}\right)`.

        Sums of the form

        .. math::
            \sum_{l=2}^{\infty}{\rm deg}(d,l)\overline{l}^{-a}

        are also returned, where

        .. math::
            {\rm deg}(d,l) =
                \frac{(d+2 l-2) \Gamma (d+l-2)}{\Gamma (d-1) \Gamma (l+1)}.

        If :math:`d=2n-2\epsilon`, then these sums contain :math:`\epsilon`
        poles if :math:`2n-2-a=-1`. In cases when this happens
        :func:`findWKB` replaces the sum with

        .. math::
            {\rm deg}(d,1) \left(d/2\right)^{-a}
            +{\rm deg}(d,2)\left(d/2+1\right)^{-a}

        The divergent sum

        .. math::
            \sum_{l=0}^{\infty}{\rm deg}(d,l)\overline{l}^{-a}

        is instead returned by :py:data:`findRenormalisationTerm`.

        If the sum is finite in dimensional regularization the code returns

        .. math::
            \lim_{\epsilon \rightarrow 0}
                \sum_{l=0}^{\infty}{\rm deg}(d,l)\overline{l}^{-a}.


        In cases where the bounce approaches the false minima as
        :math:`\phi \sim r^{-a}`,
        the routine improves the WKB approximation by approximating
        :math:`W(r) \sim W_\infty r^{-a_\infty}` for large :math:`r`

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l_max : int
            Maximum orbital quantum number.
        Delta_W_inf : float, optional
            The prefactor :math:`W_\inf` in the fit at large radii
            :math:`\Delta W \approx W_\inf r^{-a_\inf}`. Note that these
            values are only needed if the particle is massless.
        a_inf : float, optional
            The exponent :math:`a_\inf` in the fit at large radii
            :math:`\Delta W \approx W_\inf r^{-a_\inf}`. Note that these
            values are only needed if the particle is massless.
        separate_orders : boole, optional
            If True returns the terms in the WKB expansion at each power of
            :math:`1/l` separately. Default is :py:data:`False`.

        Returns
        -------
        WKB : float
           The ratio of determinants
           :math:`\log \frac{\Psi(\infty)}{\Psi_{FV}(\infty)}` up to
           :math:`l^{-9}`.

        err_WKB : float
           Estimated error on :py:data:`WKB`.

        WKBSum : float
            The sum
            :math:`\frac{1}{2}\sum_{l=2}^{\infty}{\rm deg}(d,l)\log\frac{\Psi(\infty)}{\Psi_{FV}(\infty)}`
            within the WKB approximation.

        References
        ----------
        .. [GO] Gerald V. Dunne,  Jin Hur, Choonkyu Lee,  Hyunsoo Min.
            Instanton determinant with arbitrary quark mass: WKB phase-shift
            method and derivative expansion, Phys.Lett.B 600 (2004) 302-313
        """
        config = self.__getParticleConfig(particle)
        if config.massless_Higgs and (Delta_W_inf is None or a_inf is None):
            raise ValueError(
                "Delta_W_inf and a_inf must be set if massless_Higgs is True"
            )
        return findWKB(
            config,
            l_max,
            Delta_W_inf=Delta_W_inf,
            a_inf=a_inf,
            separate_orders=separate_orders,
        )

    def findNegativeEigenvalue(self, eig_tol=1e-6):
        r"""Negative eigenvalue of the Higgs operator :math:`\mathcal{O}_H(\phi_\text{b})`

        In continuum notation, the eigenvalue equation takes the form

        .. math::
            \left(-\partial^2-\frac{d-1}{r}\partial
            +V''(\phi_\text{b})\right)f(r)=\lambda_- f(r),

        and for bubble nucleation, or vacuum decay, this operator has a single
        negative eigenvalue, some finite number of zero eigenvalues and an
        infinite number of positive eigenvalues.

        Here, we use the finite difference matrix representation of the
        differential operator accurate to :math:`1/N^4`, with two
        different boundary conditions, \"Neumann\" and \"Dirichlet\", at the maximal
        numerical radius.

        The leading, :math:`1/N^4` numerical error
        is extrapolated away using a fit to direct numerical estimates of the
        eigenvalue, and the residual error is estimated. The different boundary
        conditions provide additional information for the error estimation, appended
        to the residual numerical error.


        Parameters
        ----------
        eig_tol : float, optional
            Relative tolerance for the direct numerical eigenvalues used for the
            extrapolation.

        Returns
        -------
        res : float
            The value of the negative eigenvalue.
        err : float
            Estimated error in the result.

        """
        return findNegativeEigenvalue(self.bubble, eig_tol=eig_tol)

    def findLogPhiInfinity(self, log_phi_inf_tol=0.001, tail=0.007):
        r""" :math:`\log\phi_\infty` coefficent for the background field

        We fit for the unknown constant :math:`\phi_\infty` in the asymptotic
        behavior of the numerical bubble profile,

        .. math::
            \phi(r) \sim \phi_{\mathrm{F}}
            + \phi_\infty
            K(d/2 - 1, m_\text{F} r)\left(\frac{m_\text{F}}{r}\right)^{d/2 - 1},

        assuming the potential has a positive mass term in the false vacuum,
        :math:`\phi = \phi_{\mathrm{F}}`.

        First, we find four approximate values for the asymptotic behavior of
        the numerical bubble profile. Then, we extrapolate linearly from these
        values to a more precise and robust value than obtainable directly from
        the numerical bubble solution.

        If the bubble profile is precise near the false vacuum, i.e. at large
        radii, the argument tail can be decreased from the default of 0.015,
        which can then be used to increase the precision of the result. This
        corresponds to performing the linear extrapolation with points closer to
        the false vacuum, and correspondingly closer to the end of the profile.
        However, note that the default setting is already very precise and works
        well with the default settings of the CosmoTransitions package set in
        this package. A more detailed description for the tail parameter can be
        found from the correspoding article.

        Parameters
        ----------
        log_phi_inf_tol : float, optional
            A parameter determining an accuracy goal for the error caused by
            choosing points that are close to the end of the numerical bubble
            profile, < result * log_phi_inf_tol. If the goal cannot be met, it
            is weakened with an internal algorithm.
        tail : float, optional
            A parameter determining the chosen bubble-tail points for fitting
            the asymptotic behaviour. Shrinking tail :math:`\to 0` corresponds
            to :math:`r\to \infty` for the chosen points.

        Returns
        -------
        res : float
            The value of :math:`\log\phi_\infty`.
        err : float
            Estimated error in the result.

        """
        return findLogPhiInfinity(
            self.bubble, log_phi_inf_tol=log_phi_inf_tol, tail=tail
        )

    def findDerivativeExpansion(self, particle, NLO=False):
        r"""Derivative expansion of determinant

        The derivative expansion is an expansion in a ratio of length scales,
        which in turn can be related to a ratio of masses: the mass of the
        background scalar divided by the mass of the fluctuating field.

        The leading order (LO) and next-to-leading order (NLO) of the expansion
        are

        .. math::
            \int \mathrm{d}^d x \underbrace{\left[
                V_{(1)}(\phi_\text{b}) - V_{(1)}(\phi_\text{F})
                \right]}_\text{LO}
            + \int \mathrm{d}^d x \underbrace{\left[
                \frac{1}{2} Z_{(1)}(\phi_\text{b})
                    \nabla_\mu\phi_\text{b}\nabla_\mu\phi_\text{b}
                \right]}_\text{NLO},

        where :math:`V_{(1)}` and :math:`Z_{(1)}` are the heavy particle's
        contribution to the one-loop effective potential and field
        normalisation factor.

        Parameters
        ----------
        particle : ParticleConfig
            The heavy particle for which to carry out the derivative expansion.
            Must not have zero modes.
        NLO : boole, optional
            If :py:data:`True`, the derivative expansion is carried out to
            next-to-leading order, otherwise at leading order. Default is
            :py:data:`False`.

        Returns
        -------
        S1 : float
            The result within the derivative expasion.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findDerivativeExpansion(config, NLO=NLO)

    def __dofSpin(self, particle):
        r"""
        Returns number of spin degrees of freedom for the given particle.
        """
        if particle.spin == 0:
            return 1
        elif particle.spin == 1 and self.bubble.dim != 1:
            return self.bubble.dim - 1
        elif particle.spin == 1 and self.bubble.dim == 1:
            raise ValueError("Particle spin must be 0 in d=1")
        else:
            raise ValueError("Particle spin must be in [0, 1]")

    def __lMassRadius(self, particle):
        r"""
        Calculates product of mass and radius for determinant, to give the
        natural order of :math:`l`.
        """
        config = self.__getParticleConfig(particle)
        # natural scale for l is m*R, where m is largest relevant mass scale
        return int(config.m_max * config.r_mid)

    def __chooseLmax(self, particle, l_max=None):
        r"""
        Method for choosing a sensible value of :math:`l_\text{max}`.
        """
        if l_max is not None:
            return l_max
        dim = self.bubble.dim
        l_mR = self.__lMassRadius(particle)
        if dim < 4:
            n_mR_min = 3
            l_max_min = 25
        elif dim < 7:
            n_mR_min = dim - 1
            l_max_min = 30
        elif dim >= 7:
            n_mR_min = 12
            l_max_min = 35
        l_max_act = max(l_max_min, n_mR_min * l_mR)
        if l_max_act > 1e3:
            warnings.warn(f"{l_max_act=} > 1000", RuntimeWarning)
        return l_max_act

    def __testTruncate(self, l, l_mR, S1_array, S1_err):
        r"""
        Method to decide whether or not to truncate the sum over :math:`l`
        early, i.e. before reaching :math:`l_\text{max}`.
        """
        dim = self.bubble.dim
        if dim < 4:
            n_mR_min = 2.5
            l_max_min = 15
        elif dim < 7:
            n_mR_min = dim - 2
            l_max_min = 20
        elif dim >= 7:
            n_mR_min = 8
            l_max_min = 30
        l_max_trunc = max(l_max_min, n_mR_min * l_mR)
        if l > l_max_trunc:
            # computing measures for breaking conditions
            start = l - l_max_min // 2
            end = l + 1
            mid = (start + end) // 2
            abs_start = np.mean(abs(S1_array[start:mid]))
            abs_end = np.mean(abs(S1_array[mid:end]))
            abs_tail = np.mean(abs(S1_array[start:end]))
            err_tail = np.mean(abs(S1_err[start:end]))
            # checking if can break early
            return err_tail > abs_tail or abs_end > abs_start
        else:
            return False

    def __groupVolumeFactor(self, particle):
        r"""Calculates the volume of the broken group.

        For a symmetry-breaking pattern where G breaks down to H, the volume of
        the broken coset group is

        .. math::
            {\rm Vol}(G / H) = \frac{{\rm Vol}(G)}{{\rm Vol}(H)}.
        """
        config = self.__getParticleConfig(particle)
        group_volume = 1
        for k in config.gauge_groups[0]:
            group_volume *= group_volume(k)

        unbroken_volume = 1
        for k in config.gauge_groups[1]:
            unbroken_volume *= group_volume(k)

        return group_volume / unbroken_volume

    def __getParticleConfig(self, particle):
        if particle in self.particles:
            i_particle = self.particles.index(particle)
            return self.configs[i_particle]
        else:
            raise ValueError(
                f"Unknown ParticleConfig: {particle} not in {self.particles}"
            )

    @staticmethod
    def __degeneracy(dim, l):
        r"""
        Degeneracy of modes with fixed :math:`d` and :math:`l`.
        """
        if l == 0 or dim == 1:
            return 1
        elif dim == 3:
            return 2 * l + 1
        elif dim == 4:
            return (l + 1) ** 2
        elif dim == 2:
            return 2
        else:
            return (2 * l + dim - 2) / special.beta(l + 1, dim - 3) / (dim - 3) / (dim - 2)
