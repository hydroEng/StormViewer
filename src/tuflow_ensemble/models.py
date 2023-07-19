import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

class POLine:

    def __init__(self, id: str, event: str, data):
        """
        Constructor.

        Args:
            id: POLine name.
            event: Storm frequency (e.g. "1yr").
            duration: Storm duration.
            tps: List of temporal patterns modelled in storm package.
            data: Pandas dataframe containing maximum flows.
        """

        self.id = id
        self.event = event
        self.data = data

        self.crit_duration, self.crit_tp, self.crit_flow = self.results(data)

        self.fig = None

    def plot(self):

        fig, ax = plt.subplots()

        name = self.data.name

        tp_cols = [col for col in self.data.columns if "tp" in col]
        T_data = self.data[tp_cols].T

        ax = sns.boxplot(T_data, color="lightyellow", saturation=1.0)
        ax = sns.stripplot(T_data, palette="dark:black", jitter=0, size=3)

        ax.set_xlabel('Duration (minutes)')
        ax.set_ylabel(r"Max Flow ($\mathregular{m^{3}}$/s)")
        ax.set_title(name)

        self.fig = fig

    def results(self, data):
        """
        Process data to generate results.

        Returns:
            A tuple of critical values:  Duration, TP and Max Flow.
        """

        crit_duration = pd.to_numeric(data["Median"]).idxmax()
        crit_tp = data.loc[crit_duration, "Critical TP"]
        if crit_tp == "NA":
            crit_flow = "NA"
        else:
            crit_flow = data.loc[crit_duration, crit_tp]

        return crit_duration, crit_tp, crit_flow


    def save_results(self):
        "foo"




