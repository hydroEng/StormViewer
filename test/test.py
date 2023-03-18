import unittest
import os
import pandas as pd
from tuflow_ensemble import tuflow_ensemble


class testParsePoCSV(unittest.TestCase):
    def test_parse_po_csv(self):
        expected_output = pd.read_pickle('df_parse_po_csv.pickle')
        input_csv = os.path.join("sample_data", "Example_010.0Y_10m_tp01_001_PO.csv")
        actual_output = tuflow_ensemble.parse_po_csv(input_csv)
        pd.testing.assert_frame_equal(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
