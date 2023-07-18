class POLine:

    def __init__(self, id: str, event: str, duration: str, tps: list[str], data):
        """
        Constructor.

        Args:
            id: Storm name.
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

        duration = data["Median"].idxmax()
        tp = data.loc(duration, "Critical TP")
        if tp == "NA":
            flow = "NA"
        else:
            flow = data.loc(duration, tp)

        return duration, tp, flow




