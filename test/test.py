import unittest
import os
import pandas as pd
from StormViewer import logger, te
import pathlib

wd = pathlib.Path(__file__).parent.resolve()

sample_data = os.path.join(wd, "sample_data")


class TestParsePoCSV(unittest.TestCase):
    # This test checks that result csv file is being parsed as a dataframe
    # correctly.
    def test_parse_po_csv(self):
        expected_output = pd.read_pickle(os.path.join(wd, "df_parse_po_csv.pickle"))
        input_csv = os.path.join(sample_data, "Example_010.0Y_10m_tp01_001_PO.csv")
        actual_output = te.parse_po_csv(input_csv)
        pd.testing.assert_frame_equal(expected_output, actual_output)


class TestParseStormName(unittest.TestCase):
    # This test checks that storm names are being parsed into storm
    # frequency, duration and temp pattern correctly.
    def test_parse_storm_name(self):
        storm_name = "Example-Catchment_0.5EY_360m_tp07_no-blockages_001_PO.csv"
        expected_tuple = ("0.5ey", "360m", "tp07")
        actual_tuple = te._parse_run_id(storm_name)
        self.assertEqual(expected_tuple, actual_tuple)


class TestCritStorm(unittest.TestCase):
    # This test checks whether critical storms are being calculated properly.
    def test_critical_storm_df(self):
        df = pd.read_pickle(os.path.join(wd, "100y_sample_maxflows.pickle"))
        expected = [
            "tp07",
            "tp08",
            "tp04",
            "tp07",
            "tp06",
            "tp06",
            "tp06",
            "tp09",
            "tp10",
            "tp02",
            "tp03",
        ]
        df["Critical Storm"] = df.apply(te._get_crit_tp, axis=1)
        actual = df["Critical Storm"].tolist()
        self.assertEqual(expected, actual)


class TestLogging(unittest.TestCase):
    """This class tests logging functionality."""

    def test_list_log(self):
        df = pd.read_pickle(os.path.join(wd, "100y_sample_maxflows.pickle"))
        st = "ABC 123"
        lst = [df, st]
        log_test = logger.Logger()
        log_test.log(lst)

        # Test that end of df, and all of st show up in log string.
        assert "3.31845\n\nABC 123" in log_test.log_string


if __name__ == "__main__":
    unittest.main()
