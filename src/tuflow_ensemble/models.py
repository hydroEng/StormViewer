import pandas as pd
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

    def plot(self):
        "foo"
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




