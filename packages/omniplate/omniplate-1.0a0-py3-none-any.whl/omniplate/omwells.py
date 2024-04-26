import numpy as np

import omniplate.admin as admin
import omniplate.clogger as clogger
import omniplate.omerrors as errors
import omniplate.omgenutils as gu
import omniplate.sunder as sunder


def contentsofwells(self, wlist):
    """
    Display contents of wells.

    Parameters
    ----------
    wlist: string or list of string
        Specifies the well or wells of interest.

    Examples
    --------
    >>> p.contentsofwells(['A1', 'E4'])
    """
    wlist = gu.makelist(wlist)
    for w in wlist:
        print("\n" + w + "\n--")
        print(
            self.wellsdf.query("well == @w")
            .drop(["well"], axis=1)
            .to_string(index=False)
        )


def showwells(
    self,
    concise=False,
    sortby=False,
    experiments="all",
    conditions="all",
    strains="all",
    experimentincludes=False,
    experimentexcludes=False,
    conditionincludes=False,
    conditionexcludes=False,
    strainincludes=False,
    strainexcludes=False,
):
    """
    Display wells for specified experiments, conditions, and strains.

    Parameters
    ----------
    concise: boolean
        If True, display as experiment: condition: strain.
    sortby: list of strings, optional
        List of column names on which to sort the results.
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

    Examples
    --------
    >>> p.showwells()
    >>> p.showwells(strains= 'Mal12:GFP', conditions= '1% Mal')
    """
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
        nonull=False,
    )
    if not hasattr(self, "wellsdf"):
        self.wellsdf = admin.makewellsdf(self.r)
    df = self.wellsdf.query(
        "experiment == @exps and condition == @cons and strain == @strs"
    )
    if sortby:
        df = df.sort_values(by=gu.makelist(sortby))
    print()
    for e in exps:
        if concise:
            print(
                df[["experiment", "condition", "strain"]]
                .drop_duplicates()
                .query("experiment == @e")
                .to_string(index=False)
            )
        else:
            print(df.query("experiment == @e").to_string(index=False))
        print()


@clogger.log
def ignorewells(
    self,
    exclude=[],
    experiments="all",
    experimentincludes=False,
    experimentexcludes=False,
    clearall=False,
):
    """
    Ignore the wells specified in any future processing.

    If called several times, the default behaviour is for any previously
    ignored wells not to be re-instated.

    Parameters
    ---------
    exclude: list of strings
        List of labels of wells on the plate to be excluded.
    experiments: string or list of strings
        The experiments to include.
    experimentincludes: string, optional
        Selects only experiments that include the specified string in their
        name.
    experimentexcludes: string, optional
        Ignores experiments that include the specified string in their
        name.
    clearall: boolean
        If True, all previously ignored wells are re-instated.

    Example
    -------
    >>> p.ignorewells(['A1', 'C2'])
    """
    if clearall:
        # forget any previously ignoredwells
        self.r = self.origr.copy()
        self.progress["ignoredwells"] = {exp: [] for exp in self.allexperiments}
        admin.update_s(self)
        print(
            "Warning: all corrections and analysis to raw data have been"
            " lost. No wells have been ignored."
        )
    else:
        if gu.islistempty(exclude):
            return
        else:
            # exclude should be a list of lists
            if isinstance(exclude, str):
                exclude = [gu.makelist(exclude)]
            elif isinstance(exclude[0], str):
                exclude = [exclude]
            # check consistency
            if len(self.allexperiments) == 1:
                exps = self.allexperiments
            else:
                exps = sunder.getset(
                    self,
                    experiments,
                    experimentincludes,
                    experimentexcludes,
                    "experiment",
                    nonull=True,
                )
            if len(exclude) != len(exps) and not clearall:
                raise errors.IgnoreWells(
                    "Either a list of wells to exclude for a particular\n"
                    "experiment or a list of experiments must be given."
                )
            else:
                # drop wells
                for ex, exp in zip(exclude, exps):
                    # wells cannot be ignored twice
                    wex = list(set(ex) - set(self.progress["ignoredwells"][exp]))
                    # drop data from ignored wells
                    df = self.r
                    filt = (df["experiment"] == exp) & df["well"].isin(wex)
                    df = df.loc[~filt]
                    df = df.reset_index(drop=True)
                    self.r = df
                    # store ignoredwells
                    self.progress["ignoredwells"][exp] += ex
                    # remove any duplicates
                    self.progress["ignoredwells"][exp] = list(
                        set(self.progress["ignoredwells"][exp])
                    )
                # give warning
                anycorrections = np.count_nonzero(
                    self.sc[[col for col in self.sc.columns if "correct" in col]].values
                )
                if np.any(anycorrections):
                    print(
                        "Warning: you have ignored wells after correcting\n"
                        "the data. It is best to ignorewells first, before\n"
                        "running any analysis."
                    )
            # remake summary data
            admin.update_s(self)
