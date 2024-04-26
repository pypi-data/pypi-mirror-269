import numpy as np

import omniplate.admin as admin
import omniplate.clogger as clogger
import omniplate.omplot as omplot
import omniplate.sunder as sunder
from omniplate.runfitderiv import runfitderiv


@clogger.log
def getstats(
    self,
    dtype="OD",
    bd=False,
    cvfn="matern",
    empirical_errors=False,
    noruns=10,
    exitearly=True,
    noinits=100,
    nosamples=100,
    logs=True,
    figs=True,
    findareas=False,
    plotlocalmax=True,
    showpeakproperties=False,
    max_data_pts=None,
    experiments="all",
    experimentincludes=False,
    experimentexcludes=False,
    conditions="all",
    conditionincludes=False,
    conditionexcludes=False,
    strains="all",
    strainincludes=False,
    strainexcludes=False,
    **kwargs,
):
    """
    Smooth data, find its derivatives, and calculate summary statistics.

    The first and second time derivatives are found, typically of OD,
    using a Gaussian process (Swain et al., 2016).

    The derivatives are stored in the .s dataframe;
    summary statistics are stored in the .sc dataframe.

    Parameters
    ----------
    dtype: string, optional
        The type of data - 'OD', 'GFP', 'cGFPperOD', or 'cGFP' - for
        which the derivatives are to be found. The data must exist in the
        .r or .s dataframes.
    bd: dictionary, optional
        The bounds on the hyperparameters for the Gaussian process.
        For example, bd= {1: [-2,0])} fixes the bounds on the
        hyperparameter controlling flexibility to be 1e-2 and 1e0.
        The default for a Matern covariance function
        is {0: (-5,5), 1: (-4,4), 2: (-5,2)},
        where the first element controls amplitude, the second controls
        flexibility, and the third determines the magnitude of the
        measurement error.
    cvfn: string, optional
        The covariance function used in the Gaussian process, either
        'matern' or 'sqexp' or 'nn'.
    empirical_errors: boolean, optional
        If True, measurement errors are empirically estimated from the
        variance across replicates at each time point and so vary with
        time.
        If False, the magnitude of the measurement error is fit from the
        data assuming that this magnitude is the same at all time points.
    noruns: integer, optional
        The number of attempts made for each fit. Each attempt is made
        with random initial estimates of the hyperparameters within their
        bounds.
    exitearly: boolean, optional
        If True, stop at the first successful fit.
        If False, use the best fit from all successful fits.
    noinits: integer, optional
        The number of random attempts to find a good initial condition
        before running the optimization.
    nosamples: integer, optional
        The number of samples used to calculate errors in statistics by
        bootstrapping.
    logs: boolean, optional
        If True, find the derivative of the log of the data and should be
        True to determine the specific growth rate when dtype= 'OD'.
    figs: boolean, optional
        If True, plot both the fits and inferred derivative.
    findareas: boolean, optional
        If True, find the area under the plot of gr vs OD and the area
        under the plot of OD vs time. Setting to True can make getstats
        slow.
    plotlocalmax: boolean, optional
        If True, mark the highest local maxima found, which is used to
        calculate statistics, on any plots.
    showpeakproperties: boolean, optional
        If True, show properties of any local peaks that have found by
        scipy's find_peaks. Additional properties can be specified as
        kwargs and are passed to find_peaks.
    max_data_pts: integer, optional
        If set, sufficiently large data sets with multiple replicates will
        be subsampled at each time point, randomly picking a smaller
        number of replicates, to reduce the number of data points and so
        run times.
    experiments: string or list of strings
        The experiments to include.
    conditions: string or list of strings
        The conditions to include.
    strains: string or list of strings
        The strains to include.
    experimentincludes: string, optional
        Selects only experiments that include the specified string in their
        name.
    experimentexcludes: string, optional
        Ignores experiments that include the specified string in their
        name.
    conditionincludes: string, optional
        Selects only conditions that include the specified string in their
        name.
    conditionexcludes: string, optional
        Ignores conditions that include the specified string in their name.
    strainincludes: string, optional
        Selects only strains that include the specified string in their
        name.
    strainexcludes: string, optional
        Ignores strains that include the specified string in their name.
    kwargs: for scipy's find_peaks
        To set the minimum property of a peak. e.g. prominence= 0.1 and
        width= 15 (specified in numbers of x-points or y-points and not
        real units).
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

    Examples
    --------
    >>> p.getstats()
    >>> p.getstats(conditionincludes= 'Gal')
    >>> p.getstats(noruns= 10, exitearly= False)

    If the fits are poor, often changing the bounds on the hyperparameter
    for the measurement error helps:

    >>> p.getstats(bd= {2: (-3,0)})

    References
    ----------
    PS Swain, K Stevenson, A Leary, LF Montano-Gutierrez, IB Clark,
    J Vogel, T Pilizota. (2016). Inferring time derivatives including cell
    growth rates using Gaussian processes. Nat Commun, 7, 1-8.
    """
    admin.check_kwargs(kwargs)
    linalgmax = 5
    warnings = ""
    # variable to be fit
    if logs:
        fitvar = f"log_{dtype}"
    else:
        fitvar = dtype
    # name of derivative of fit variable
    if fitvar == "log_OD":
        derivname = "gr"
    else:
        derivname = f"d/dt_{fitvar}"
    # extract data
    exps, cons, strs = sunder.getall(
        self,
        experiments,
        experimentincludes,
        experimentexcludes,
        conditions,
        conditionincludes,
        conditionexcludes,
        strains,
        strainincludes,
        strainexcludes,
        nonull=True,
    )
    # find growth rate and stats
    for e in exps:
        for c in cons:
            for s in strs:
                esc_name = f"{e}: {s} in {c}"
                if f"{s} in {c}" in self.allstrainsconditions[e]:
                    if dtype in self.r.columns:
                        # raw data
                        t, d = sunder.extractwells(
                            self.r, self.s, e, c, s, dtype
                        )
                    elif dtype in self.s.columns:
                        # processed data
                        df = self.s.query(
                            "experiment == @e and condition == @c and "
                            "strain == @s"
                        )
                        # add columns plus and minus err
                        df = omplot.augmentdf(df, dtype)[
                            [dtype, "augtype", "time"]
                        ]
                        piv_df = df.pivot(
                            index="time", columns="augtype", values=dtype
                        )
                        # convert to array for fitderiv
                        d = piv_df.values
                        t = piv_df.index.to_numpy()
                        numberofnans = np.count_nonzero(np.isnan(d))
                        if np.any(numberofnans):
                            print(f"\nWarning: {numberofnans} NaNs in data")
                    else:
                        print(f"\n-> {dtype} not recognised for {esc_name}.\n")
                        return
                    # checks
                    if d.size == 0:
                        # no data
                        if (
                            esc_name.split(":")[1].strip()
                            in self.allstrainsconditions[e]
                        ):
                            print(
                                f"\n-> No data found for {dtype} for {esc_name}.\n"
                            )
                        continue
                    # run fit
                    _, warning = runfitderiv(
                        self,
                        t,
                        d,
                        fitvar,
                        derivname,
                        e,
                        c,
                        s,
                        bd=bd,
                        cvfn=cvfn,
                        empirical_errors=empirical_errors,
                        noruns=noruns,
                        exitearly=exitearly,
                        noinits=noinits,
                        nosamples=nosamples,
                        logs=logs,
                        figs=figs,
                        findareas=findareas,
                        plotlocalmax=plotlocalmax,
                        showpeakproperties=showpeakproperties,
                        linalgmax=linalgmax,
                        max_data_pts=max_data_pts,
                        **kwargs,
                    )
                    if warning:
                        warnings += warning
    if warnings:
        print(warnings)
