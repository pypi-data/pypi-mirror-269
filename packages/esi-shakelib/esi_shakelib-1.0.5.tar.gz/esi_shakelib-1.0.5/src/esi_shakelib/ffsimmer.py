"""
Perform Monte Carlo simulation of  finite faults and perform a mixed effects
regression to obtain mean ground motions and uncertainties.
"""

import copy
from enum import Enum
import warnings

import numpy as np
import statsmodels.formula.api as smf
from statsmodels.tools.sm_exceptions import ConvergenceWarning
import pandas as pd
from scipy.stats import norm

import openquake.hazardlib.const as oqconst
from esi_utils_rupture.quad_rupture import QuadRupture
from esi_utils_rupture.point_rupture import PointRupture
from esi_utils_rupture.distance import Distance
from esi_shakelib.sites import Sites


class AutoName(Enum):
    """
    These enum members hold their name (as a string) as their value.
    For example: DistType.Rjb.value == 'Rjb'
    """

    def __init__(self):
        self._value_ = self.name


class DistType(AutoName):
    """
    Type of distance measure to compute.
       - 'Rjb' is for the Joyner-Boore distance.
       - 'Rrup' is for closest distance to rupture.
    """

    Rjb = ()
    Rrup = ()


class MagScaling(AutoName):
    """
    Magnitude scaling relationship.
       - 'WC94' is for Wells and Coppersmith (1999)
       - 'HB08' is for Hanks and Bakun (2008)
       - 'S14' is for Somerville et al. (2014)
       - 'Sea10_interface' is for Strasser et al. (2010), for interface events
       - 'Sea10_slab' is for Strasser et al. (2010), for intraplate events
    """

    WC94 = ()
    HB08 = ()
    S14 = ()
    Sea10_interface = ()
    Sea10_slab = ()


class Mechanism(AutoName):
    """
    Source mechanism.
       - 'A' for all (mechanism is unknown/unspecified)
       - 'R' for reverse
       - 'N' for normal
       - 'SS' for strike-slip
    """

    A = ()
    R = ()
    N = ()
    SS = ()


class FFSimmer:
    """
    Class to perform monte carlo simulations of finite faults to derive mean ground
    motions
    """

    def __init__(self, origin, rff):
        """
        origin: (Origin object)
            The earthquake origin
        gmpe: (MultiGMPE object)
            The MultiGMPE to be used for the simulations
        rff: (RandomFiniteFault object)
            An object initialized to a set of random faults
        nsim: (int)
            The number of simulations to perform
        """
        warnings.simplefilter("ignore", ConvergenceWarning)
        self.origin = copy.copy(origin)
        self.rff = rff

    def compute_grid(self, grid, gmpes, myimts):
        """
        Args:
            grid: (Grid2D object)
                Basically the vs30grid that we're mapping, used for its dimensions.
                The site corrections have to be done elsewhere.
            myimts (list)
                List of OQ IMTs to generate grids and transects for
        """
        griddict = {}
        hypo = self.origin.getHypo()
        olon = hypo.x
        olat = hypo.y

        sd_types = list(gmpes[myimts[0]].DEFINED_FOR_STANDARD_DEVIATION_TYPES)

        #
        gd = grid.getGeoDict()
        # Increase the grid resolution if it is greater the 30 arc-seconds
        delta_y = gd.dy
        if delta_y > (30.0 / 3600.0):
            delta_y = delta_y / 2.0
        # Compute distance to all four corners of grid
        prup = PointRupture(self.origin)
        lons = np.array([gd.xmin, gd.xmin, gd.xmax, gd.xmax])
        lats = np.array([gd.ymin, gd.ymax, gd.ymin, gd.ymax])
        depths = np.zeros_like(lons)
        repi = prup.computeRepi(lons, lats, depths)
        rmax = np.max(repi)

        west = olon
        east = olon
        south = olat
        north = olat + rmax / 111.1
        if north > 90.0:
            north = olat
            south = olat - rmax / 111.1

        sites = Sites.fromBounds(
            west,
            east,
            south,
            north,
            delta_y,
            delta_y,
            defaultVs30=760.0,
            vs30File=None,
            padding=True,
            resample=True,
        )
        (nx, ny) = sites.getNxNy()
        sgd = sites.getVs30Grid().getGeoDict()
        sctx = sites.getSitesContext()
        for k, v in sctx.__dict__.items():
            if k == "_slots_":
                continue
            sctx.__dict__[k] = sctx.__dict__[k].flatten()

        nsim = self.rff.get_nsim()
        nimt = len(myimts)
        means = np.empty((nimt, nsim, nx * ny))
        sigs = np.empty((nimt, nsim, nx * ny))
        if len(sd_types) > 1:
            taus = np.empty((nimt, nsim, nx * ny))
            phis = np.empty((nimt, nsim, nx * ny))

        for idx in range(nsim):
            rupt = self.rff.retrieve_rupt(idx)
            dist = Distance.fromSites(gmpes[myimts[0]], sites, rupt)
            dctx = dist.getDistanceContext()
            for k, v in dctx.__dict__.items():
                if k == "_slots_":
                    continue
                if not isinstance(dctx.__dict__[k], np.ndarray):
                    continue
                dctx.__dict__[k] = dctx.__dict__[k].flatten()
            rctx = rupt.getRuptureContext(gmpes[myimts[0]])

            for iimt, simt in enumerate(myimts):
                mean, stddevs = gmpes[simt].get_mean_and_stddevs(
                    sctx, rctx, dctx, simt, sd_types
                )
                means[iimt, idx, :] = mean[0]
                sigs[iimt, idx, :] = stddevs[0][0]
                if len(sd_types) > 1:
                    taus[iimt, idx, :] = stddevs[1][0]
                    phis[iimt, idx, :] = stddevs[2][0]

        slat = np.linspace(sgd.ymin, sgd.ymax, sgd.ny)
        repi = prup.computeRepi(
            np.full_like(slat, sgd.xmin),
            slat,
            np.zeros_like(slat),
        )

        gd = grid.getGeoDict()
        glon, glat = np.meshgrid(
            np.linspace(gd.xmin, gd.xmax, gd.nx),
            np.linspace(gd.ymin, gd.ymax, gd.ny),
        )
        gdepth = np.zeros_like(glon)
        grepi = rupt.computeRepi(glon, glat, gdepth)

        # Compute Mean, Sigma, Phi, and Tau for each IMT
        mean_residuals = np.empty((nsim, nx * ny))
        distances = np.empty((nsim, nx * ny))
        for iimt in range(nimt):
            mean_means = np.mean(means[iimt], axis=0)
            for idx in range(nsim):
                mean_residuals[idx] = means[iimt, idx] - mean_means
                distances[idx, :] = idx
            extra_sigmas = np.var(means[iimt], axis=0)

            df = pd.DataFrame(
                {
                    "residual": mean_residuals.flatten(),
                    "distances": distances.flatten(),
                }
            )
            mod = smf.mixedlm("residual ~ 1", df, groups=df["distances"])
            try:
                mod_fit = mod.fit()
            except Exception:
                print("Error in mixedlm.fit")
                # Don't have an answer, so just guess
                avg_extra_tau = 0.80
                avg_extra_phi = 0.20
            else:
                avg_extra_tau = mod_fit.cov_re.Group.Group
                avg_extra_phi = mod_fit.scale

            if (
                np.isnan(avg_extra_tau)
                or np.isnan(avg_extra_phi)
                or avg_extra_tau < 1e-8
                or avg_extra_phi < 1e-8
            ):
                print("mixedlm.fit produced unusable results")
                avg_extra_tau = 0.80
                avg_extra_phi = 0.20

            avg_tau_wgt = avg_extra_tau / (avg_extra_tau + avg_extra_phi)
            avg_phi_wgt = 1.0 - avg_tau_wgt
            extra_taus = avg_tau_wgt * extra_sigmas
            extra_phis = avg_phi_wgt * extra_sigmas

            # Take the mean over the realizations
            mean_sigs = np.sqrt(np.mean(sigs[iimt] ** 2, axis=0) + extra_sigmas)
            if len(sd_types) > 1:
                mean_taus = np.sqrt(np.mean(taus[iimt] ** 2, axis=0) + extra_taus)
                mean_phis = np.sqrt(np.mean(phis[iimt] ** 2, axis=0) + extra_phis)

            griddict[myimts[iimt]] = {
                "mean": np.interp(grepi, repi, np.flip(mean_means)),
                oqconst.StdDev.TOTAL: np.interp(grepi, repi, np.flip(mean_sigs)),
                "transect": np.flip(mean_means),
                "repi": repi,
            }
            if len(sd_types) > 1:
                griddict[myimts[iimt]][oqconst.StdDev.INTER_EVENT] = np.interp(
                    grepi, repi, np.flip(mean_taus)
                )
                griddict[myimts[iimt]][oqconst.StdDev.INTRA_EVENT] = np.interp(
                    grepi, repi, np.flip(mean_phis)
                )

        return griddict

    def compute_points(self, sctx, gmpe, myimts, rock_vs30=760.0, soil_vs30=180.0):
        """
        Args:
            sctx: (Sites object)
                A sites context object set up for the points being output
            gmpe: (MultiGMPE object)
                The gmpe to perform the ground-motion realizations.
            myimts (list)
                List of OQ IMTs to generate rock and site amplified values for

        Returns:
            dictionary:
                "rock": The sites at a reference rock vs30 of 760 m/s
                "soil": The sites amplified at their given vs30
        """
        outdict = {}

        sd_types = list(gmpe.DEFINED_FOR_STANDARD_DEVIATION_TYPES)

        sctx_rock = copy.deepcopy(sctx)
        sctx_rock.vs30 = np.full_like(sctx.vs30, rock_vs30)
        sctx_soil = copy.deepcopy(sctx)
        sctx_soil.vs30 = np.full_like(sctx.vs30, soil_vs30)

        nporig = np.size(sctx.lons)
        sx = copy.deepcopy(sctx)
        for k, v in sctx.__dict__.items():
            if k == "_slots_":
                continue
            sx.__dict__[k] = np.hstack(
                (sctx.__dict__[k], sctx_rock.__dict__[k], sctx_soil.__dict__[k])
            )
        sx.sids = np.array(list(range(len(sx.lons))))
        depths = np.zeros_like(sx.lons)

        nsd = len(sd_types)
        ctxt_names = ("site", "soil", "rock")
        ctxts = (sctx, sctx_soil, sctx_rock)
        nctx = len(ctxts)

        nimt = len(myimts)
        nsim = self.rff.get_nsim()

        means = np.empty((nctx, nimt, nsim, nporig))
        sigs = np.empty((nctx, nimt, nsim, nporig))
        if len(sd_types) > 1:
            taus = np.empty((nctx, nimt, nsim, nporig))
            phis = np.empty((nctx, nimt, nsim, nporig))

        for idx in range(nsim):
            rupt = self.rff.retrieve_rupt(idx)
            dist_obj = Distance(gmpe, sx.lons, sx.lats, depths, rupt)
            dctx = dist_obj.getDistanceContext()
            rctx = rupt.getRuptureContext(gmpe)

            mean, stddevs = gmpe.get_mean_and_stddevs(sx, rctx, dctx, myimts, sd_types)
            for iimt, _ in enumerate(myimts):
                for ictx in range(nctx):
                    means[ictx, iimt, idx, :] = mean[iimt][
                        ictx * nporig : (ictx + 1) * nporig
                    ]
                    sigs[ictx, iimt, idx, :] = stddevs[iimt * nsd][
                        ictx * nporig : (ictx + 1) * nporig
                    ]
                    if len(sd_types) > 1:
                        taus[ictx, iimt, idx, :] = stddevs[iimt * nsd + 1][
                            ictx * nporig : (ictx + 1) * nporig
                        ]
                        phis[ictx, iimt, idx, :] = stddevs[iimt * nsd + 2][
                            ictx * nporig : (ictx + 1) * nporig
                        ]

        # Compute Mean, Sigma, Phi, and Tau for each IMT
        mean_residuals = np.empty((nsim, nporig))
        distances = np.empty((nsim, nporig))
        for iimt in range(nimt):
            outdict[myimts[iimt]] = {}
            for ictx, ctx_name in enumerate(ctxt_names):
                # Take the mean over the realizations
                mean_means = np.mean(means[ictx, iimt], axis=0)
                # Compute the residuals at each distance, index the distances
                for idx in range(nsim):
                    mean_residuals[idx] = means[ictx, iimt, idx] - mean_means
                    distances[idx, :] = idx
                # Find the variance over the realizations
                extra_sigmas = np.var(means[ictx, iimt], axis=0)

                # Do the mixed effects regression
                df = pd.DataFrame(
                    {
                        "residual": mean_residuals.flatten(),
                        "distances": distances.flatten(),
                    }
                )
                mod = smf.mixedlm("residual ~ 1", df, groups=df["distances"])
                try:
                    mod_fit = mod.fit()
                except Exception:
                    print("Error in mixedlm.fit")
                    # Don't have an answer, so just guess
                    avg_extra_tau = 0.80
                    avg_extra_phi = 0.20
                else:
                    avg_extra_tau = mod_fit.cov_re.Group.Group
                    avg_extra_phi = mod_fit.scale

                if (
                    np.isnan(avg_extra_tau)
                    or np.isnan(avg_extra_phi)
                    or avg_extra_tau < 1e-8
                    or avg_extra_phi < 1e-8
                ):
                    print("mixedlm.fit produced unusable results")
                    avg_extra_tau = 0.80
                    avg_extra_phi = 0.20

                avg_tau_wgt = avg_extra_tau / (avg_extra_tau + avg_extra_phi)
                avg_phi_wgt = 1.0 - avg_tau_wgt
                extra_taus = avg_tau_wgt * extra_sigmas
                extra_phis = avg_phi_wgt * extra_sigmas

                mean_sigs = np.sqrt(
                    np.mean(sigs[ictx, iimt] ** 2, axis=0) + extra_sigmas
                )
                if len(sd_types) > 1:
                    mean_taus = np.sqrt(
                        np.mean(taus[ictx, iimt] ** 2, axis=0) + extra_taus
                    )
                    mean_phis = np.sqrt(
                        np.mean(phis[ictx, iimt] ** 2, axis=0) + extra_phis
                    )

                outdict[myimts[iimt]].update(
                    {
                        ctx_name: {
                            "mean": mean_means.reshape(sctx.lons.shape),
                            oqconst.StdDev.TOTAL: mean_sigs.reshape(sctx.lons.shape),
                        }
                    }
                )
                if len(sd_types) > 1:
                    outdict[myimts[iimt]][ctx_name][oqconst.StdDev.INTER_EVENT] = (
                        mean_taus.reshape(sctx.lons.shape)
                    )
                    outdict[myimts[iimt]][ctx_name][oqconst.StdDev.INTRA_EVENT] = (
                        mean_phis.reshape(sctx.lons.shape)
                    )
        return outdict


class RandomFiniteFault(object):
    """
    Class to dole out random finite faults efficiently.
    """

    def __init__(self, origin, nsim):
        """
        Args:
            origin (Origin objece)
        """
        self.origin = origin
        self.nsim = nsim
        self.rupts = []
        self.initialize()

    def initialize(self):
        """
        Initialize the random arrays
        """
        (mscale, aspect, mindip_deg, maxdip_deg) = get_scaling_params(self.origin)
        _, _, _, _, area_mean, area_std = dimensions_from_magnitude(
            self.origin.mag, mscale, 1, 0
        )
        hypo = self.origin.getHypo()
        area = 10 ** np.random.normal(np.log10(area_mean[0]), area_std, self.nsim)
        width = np.sqrt(area / aspect)
        length = aspect * width
        dx = np.random.uniform(0, length)
        strike = np.random.uniform(-180, 180, self.nsim)
        dip = np.radians(np.random.uniform(mindip_deg, maxdip_deg, self.nsim))
        # Need to apply a max to dy that might be less than width based on the
        # eq depth.
        # H = vertical projection of plane
        # sin(dip) = H/W
        # H = W sin(dip)
        height = width * np.sin(dip)
        #  -----
        #  \   |
        #   \  | dz
        # dy \ |
        #     \|
        # sin(dip) = dz / dy
        # top_of_rupture = depth - dz so
        # depth - dz > 0
        # depth > dz
        dz = np.random.uniform(0, np.minimum(height, hypo.z))
        dy = dz / np.sin(dip)
        hx = np.array([hypo.x])
        hy = np.array([hypo.y])
        hz = np.array([hypo.z])

        for idx in range(self.nsim):
            self.rupts.append(
                QuadRupture.fromOrientation(
                    hx,
                    hy,
                    hz,
                    [dx[idx]],
                    [dy[idx]],
                    [length[idx]],
                    [width[idx]],
                    [strike[idx]],
                    [np.degrees(dip[idx])],
                    self.origin,
                )
            )

    def retrieve_rupt(self, isim):
        """
        Retrieve one fault.
        """
        if isim > self.nsim:
            raise IndexError(
                f"RandomFiniteFault.retrieve_rupt {isim=} exceeds maximum {self.nsim}"
            )
        return self.rupts[isim]

    def get_nsim(self):
        """
        Get the number of simulated faults that this object holds.
        """
        return self.nsim


def get_scaling_params(origin):
    """

    Args:
        origin:
            An Origin object.
    """

    mech = getattr(origin, "mech", "ALL")
    if not hasattr(origin, "_tectonic_region"):
        mscale = MagScaling.WC94
        # smech = Mechanism.A
        mindip_deg = 35.0
        maxdip_deg = 90.0
        aspect = 1.7
    elif origin._tectonic_region == "Active":
        mscale = MagScaling.HB08
        aspect = 1.7
        if mech == "ALL":
            # HB08 doesn't have an 'ALL' mechanism, so use WC94
            mscale = MagScaling.WC94
            # smech = Mechanism.A
            mindip_deg = 35.0
            maxdip_deg = 90.0
        elif mech == "RS":
            # smech = Mechanism.R
            mindip_deg = 35.0
            maxdip_deg = 50.0
        elif mech == "NM":
            # smech = Mechanism.N
            mindip_deg = 40.0
            maxdip_deg = 60.0
        elif mech == "SS":
            # smech = Mechanism.SS
            mindip_deg = 75.0
            maxdip_deg = 90.0
    elif origin._tectonic_region == "Stable":
        mscale = MagScaling.S14
        aspect = 1.0
        if mech == "ALL":
            # smech = Mechanism.A
            mindip_deg = 35.0
            maxdip_deg = 90.0
        elif mech == "RS":
            # smech = Mechanism.R
            mindip_deg = 35.0
            maxdip_deg = 60.0
        elif mech == "NM":
            # smech = Mechanism.N
            mindip_deg = 40.0
            maxdip_deg = 60.0
        elif mech == "SS":
            # smech = Mechanism.SS
            mindip_deg = 60.0
            maxdip_deg = 90.0
    elif origin._tectonic_region == "Subduction":
        aspect = 1.7
        if mech == "ALL":
            mscale = MagScaling.Sea10_interface
            # smech = Mechanism.A
            mindip_deg = 35.0
            maxdip_deg = 90.0
        elif mech == "RS":
            mscale = MagScaling.Sea10_interface
            # smech = Mechanism.R
            mindip_deg = 35.0
            maxdip_deg = 50.0
        elif mech == "NM":
            mscale = MagScaling.Sea10_slab
            # smech = Mechanism.N
            mindip_deg = 40.0
            maxdip_deg = 60.0
        elif mech == "SS":
            mscale = MagScaling.Sea10_slab
            # smech = Mechanism.SS
            mindip_deg = 75.0
            maxdip_deg = 90.0
    else:
        print(
            "Unsupported tectonic region; using coefficients for unknown"
            "tectonic region."
        )
        mscale = MagScaling.WC94
        # smech = Mechanism.A
        aspect = 1.7
        mindip_deg = 35.0
        maxdip_deg = 90.0

    return (mscale, aspect, mindip_deg, maxdip_deg)


def dimensions_from_magnitude(M, rup_dim_model, neps, trunc, mech=Mechanism.A):
    """
    Compute dimensions of rupture from magnitude for a specified
    magnitude scaling relation.

    Args:
        M (float): Magnitude.
        rup_dim_model (MagScaling enum): Specifies the model for compputing the
            rupture dimensions from magnitude.
        neps (int): The number of steps to integrate from -trunc to +trunc.
            Larger numbers increase the accuracy of the result, but take
            longer to run.
        trunc (float): For the integration in area (or length and width), trunc
            is the truncation of the normal distribution (in units of sigma).
        mech (Mechanism enum): Optional string indicating earthquake
            mechanism, used by some of the models.

    Returns:
        tuple: A tuple containing the following, noting that some of these will
        be empty if the selected model does not provide them:

                - length: rupture length (km).
                - sig_length: standard deviation of rupture length.
                - W: rupture width (km).
                - sigw: standard devation of rupture width.
                - A: rupture area (km).
                - siga: standard deivaiton of rupture area.

    """
    epsmid, peps, d_eps = compute_epsilon(neps, trunc)
    if not isinstance(rup_dim_model, MagScaling):
        raise TypeError("rup_dim_model must be of type MagScaling")
    if not isinstance(mech, Mechanism):
        raise TypeError("mech must be of type Mechanism")

    if rup_dim_model is MagScaling.WC94:
        # Use mech to get either M-A or (M-W) and (M-R) from Wells and
        # Coppersmith.
        if mech is Mechanism.SS:
            sig_length = 0.15
            length = 10 ** (-2.57 + 0.62 * M + sig_length * epsmid)
            sig_width = 0.14
            width = 10 ** (-0.76 + 0.27 * M + sig_width * epsmid)
            sig_area = 0.22
            area = 10 ** (-3.42 + 0.90 * M + sig_area * epsmid)
        elif mech is Mechanism.R:
            sig_length = 0.16
            length = 10 ** (-2.42 + 0.58 * M + sig_length * epsmid)
            sig_width = 0.15
            width = 10 ** (-1.61 + 0.41 * M + sig_width * epsmid)
            sig_area = 0.26
            area = 10 ** (-3.99 + 0.98 * M + sig_area * epsmid)
        elif mech is Mechanism.N:
            sig_length = 0.17
            length = 10 ** (-1.88 + 0.50 * M + sig_length * epsmid)
            sig_width = 0.12
            width = 10 ** (-1.14 + 0.35 * M + sig_width * epsmid)
            sig_area = 0.22
            area = 10 ** (-2.78 + 0.82 * M + sig_area * epsmid)
        elif mech is Mechanism.A:
            sig_length = 0.16
            length = 10 ** (-2.44 + 0.59 * M + sig_length * epsmid)
            sig_width = 0.15
            width = 10 ** (-1.01 + 0.32 * M + sig_width * epsmid)
            sig_area = 0.24
            area = 10 ** (-3.49 + 0.91 * M + sig_area * epsmid)
        else:
            raise TypeError("Unsupported value of 'mech'")
    elif rup_dim_model is MagScaling.S14:
        # Somerville (2014) model:
        #     - No length or width
        #     - No mechanism dependence
        sig_area = 0.3
        area = 10 ** (M - 4.25 + sig_area * epsmid)
        length = None
        sig_length = None
        width = None
        sig_width = None
    elif rup_dim_model == MagScaling.HB08:
        # Hanks and Bakun (2008)
        # These are the equations reported in the paper:
        #     M =       log10(A) + 3.98   for A <= 537 km^2 w/ se=0.03
        #     M = 4/3 * log10(A) + 3.07   for A >  537 km^2 w/ se=0.04
        # Using them is not so straight-forward beacuse we need to compute
        # the area from magnitude. Of course, this gives a different result
        # than if the equations were regressed for A as a function of M,
        # although since the equations were derived theoretically, this may
        # not be so bad.
        #
        # The inverted equation is simple enough:
        #     log10(A) =      M - 3.98    for M <= 6.71
        #     log10(A) = 3/4*(M - 3.07))  for M > 6.71
        #
        # The standard deviations are a little trickier.
        # First, convert standard errors of M to standard deviations of M:
        # (by my count, n=62 for A<=537, and n=28 for A>537)
        #     0.03*sqrt(62) = 0.236       for M <= 6.71
        #     0.04*sqrt(28) = 0.212       for M > 6.71
        # And convert to standard deviations of log(A) using the partial
        # derivatives
        #     dM/d(log10(A)) = 1          for M <= 6.71
        #     dM/d(log10(A)) = 3/4        for M >  6.71
        # So
        #     0.236*1   = 0.236 (pretty close to WC94)
        #     0.212*3/4 = 0.159 (seems a bit low...)
        if M > 6.71:
            sig_area = 0.236
            area = 10 ** (3 / 4 * (M - 3.07) + sig_area * epsmid)
        else:
            sig_area = 0.159
            area = 10 ** ((M - 3.98) + sig_area * epsmid)
        length = None
        sig_length = None
        width = None
        sig_width = None
    elif rup_dim_model == MagScaling.Sea10_interface:
        # Strasser et al. (2010), coefficients for interface events
        sig_length = 0.18
        length = 10 ** (-2.477 + 0.585 * M + sig_length * epsmid)
        sig_width = 0.173
        width = 10 ** (-0.882 + 0.351 * M + sig_width * epsmid)
        sig_area = 0.304
        area = 10 ** (-3.49 + 0.952 * M + sig_area * epsmid)
    elif rup_dim_model == MagScaling.Sea10_slab:
        # Strasser et al. (2010), coefficients for slab events
        sig_length = 0.146
        length = 10 ** (-2.35 + 0.562 * M + sig_length * epsmid)
        sig_width = 0.067
        width = 10 ** (-1.058 + 0.356 * M + sig_width * epsmid)
        sig_area = 0.184
        area = 10 ** (-3.225 + 0.89 * M + sig_area * epsmid)
    else:
        raise TypeError("Unsupported value of 'rup_dim_model'")
    return length, sig_length, width, sig_width, area, sig_area


def compute_epsilon(neps, trunc):
    """
    Compute midpoints and probabilities of epsilon bins.

    Args:
        neps (int): The number of steps to integrate from -trunc to +trunc.
            Larger numbers increase the accuracy of the result, but take
            longer to run.
        trunc (float): For the integration in area (or length and width), trunc
            is the truncation of the normal distribution (in units of sigma).
    Returns:
        tuple: epsilon midpoints, their probabilities, bin width.
    """
    # Need to assume a truncation level for normal distribution
    eps = np.linspace(-trunc, trunc, neps + 1)
    epsmid = 0.5 * (eps[1:] + eps[:-1])
    peps = norm.cdf(eps[1:]) - norm.cdf(eps[:-1])

    # define delta epsilons to normalize probabilities
    d_eps = 2 * trunc / neps
    epsfac = np.trapz(peps, dx=d_eps)

    if neps > 1:
        peps /= epsfac
    return epsmid, peps, d_eps
