from pathlib import Path

import numpy as np
import pandas as pd

import omniplate.admin as admin
import omniplate.clogger as clogger
import omniplate.omgenutils as gu


def savelog(self, fname=None):
    """
    Save log to file.

    Parameters
    --
    fname: string, optional
        The name of the file. If unspecified, the name of the experiment.

    Example
    -------
    >>> p.savelog()
    """
    # export log
    if fname:
        fnamepath = self.wdirpath / (fname + ".log")
    else:
        fnamepath = self.wdirpath / ("".join(self.allexperiments) + ".log")
    with fnamepath.open("w") as f:
        f.write(self.logstream.getvalue())
    print("Exported successfully.")


@clogger.log
def exportdf(self, fname=False, type="tsv", ldirec=False):
    """
    Export the dataframes.

    The exported data may either be tab-delimited or csv or json files.
    Dataframes for the (processed) raw data, for summary data, and for
    summary statistics and corrections, as well as a log file, are
    exported.

    Parameters
    ----------
    fname: string, optional
        The name used for the output files.
        If unspecified, the experiment or experiments is used.
    type: string
        The type of file for export, either 'json' or 'csv' or 'tsv'.
    ldirec: string, optional
        The directory to write. If False, the working directory is used.

    Examples
    --------
    >>> p.exportdf()
    >>> p.exportdf('processed', type= 'json')
    """
    if not fname:
        fname = "".join(self.allexperiments)
    if ldirec:
        ldirec = Path(ldirec)
        fullfname = str(ldirec / fname)
    else:
        fullfname = str(self.wdirpath / fname)
    # export data
    if type == "json":
        self.r.to_json(fullfname + "_r.json", orient="split")
        self.s.to_json(fullfname + "_s.json", orient="split")
        self.sc.to_json(fullfname + "_sc.json", orient="split")
    else:
        sep = "\t" if type == "tsv" else ","
        self.r.to_csv(fullfname + "_r." + type, sep=sep, index=False)
        self.s.to_csv(fullfname + "_s." + type, sep=sep, index=False)
        self.sc.to_csv(fullfname + "_sc." + type, sep=sep, index=False)
    # export log to file
    self.savelog(fname)


@clogger.log
def importdf(self, commonnames, info=True, sep="\t"):
    """
    Import dataframes saved as either json or csv or tsv files.

    Parameters
    ----------
    commonnames: list of strings
        A list of names for the files to be imported with one string for
        each experiment.

    Examples
    --------
    >>> p.importdf('Gal')
    >>> p.importdf(['Gal', 'Glu', 'Raf'])
    """
    commonnames = gu.makelist(commonnames)
    # import data (uses pandas but implicitly - there directly call pd.__version__)
    pd.__version__
    for commonname in commonnames:
        commonname = str(self.wdirpath / commonname)
        for df in ["r", "s", "sc"]:
            try:
                # json files
                exec(
                    "impdf= pd.read_json(commonname + '_' + df + "
                    "'.json', orient= 'split')"
                )
                print("Imported", commonname + "_" + df + ".json")
            except FileNotFoundError:
                try:
                    # csv files
                    exec(
                        "impdf= pd.read_csv(commonname + '_' + df + "
                        "'.csv', sep= ',')"
                    )
                    print("Imported", commonname + "_" + df + ".csv")
                except FileNotFoundError:
                    try:
                        # tsv files
                        exec(
                            "impdf= pd.read_csv(commonname + '_' + df "
                            "+ '.tsv', sep= '\t')"
                        )
                        print("Imported", commonname + "_" + df + ".tsv")
                    except FileNotFoundError:
                        print(
                            f"No file called {commonname}_{df}.json "
                            "or .csv or .tsv found"
                        )
                        return
            # ensure all are imported as strings
            for var in ["experiment", "condition", "strain"]:
                exec("impdf[var]= impdf[var].astype(str)")
            # merge dataframes
            if hasattr(self, df):
                exec(
                    "self."
                    + df
                    + "= pd.merge(self."
                    + df
                    + ", impdf, how= 'outer')"
                )
            else:
                exec("self." + df + "= impdf")
        print()

    # update attributes
    self.allexperiments = list(self.s.experiment.unique())
    self.allconditions.update(
        {
            e: list(self.s[self.s.experiment == e].condition.unique())
            for e in self.allexperiments
        }
    )
    self.allstrains.update(
        {
            e: list(self.s[self.s.experiment == e].strain.unique())
            for e in self.allexperiments
        }
    )
    for e in self.allexperiments:
        rdf = self.r[self.r.experiment == e]
        res = list((rdf.strain + " in " + rdf.condition).dropna().unique())
        res = [r for r in res if r != "nan in nan"]
        self.allstrainsconditions.update({e: res})

    # find datatypes with mean in self.s
    dtypdict = {}
    for e in self.allexperiments:
        # drop columns of NaNs - these are created by merge if a datatype
        # is in one experiment but not in another
        tdf = self.s[self.s.experiment == e].dropna(axis=1, how="all")
        dtypdict[e] = list(tdf.columns[tdf.columns.str.contains("mean")])
    self.datatypes.update(
        {e: [dt.split("_mean")[0] for dt in dtypdict[e]] for e in dtypdict}
    )
    # initialise progress
    for e in self.allexperiments:
        admin.initialiseprogress(self, e)
    # display info on import
    if info:
        self.info

    # display warning if duplicates created
    if len(self.allexperiments) != np.unique(self.allexperiments).size:
        print(
            "\nLikely ERROR: data with the same experiment, condition, "
            "strain, and time now appears twice!!"
        )


def save(self, name):
    """Remind user that save is undefined."""
    print("You probably mean exportdf.")
