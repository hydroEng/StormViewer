import os
from pathlib import Path
import pandas
import pandas as pd
import re

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

input_dir = r"/home/Taha/tuflow_ensemble/C01/"


def get_po_csvs(input_dir: str) -> list:
    """
    This function detects TUFLOW PO csv outputs and saves their filepaths in a list

    Args:
        input_dir (str): Path to folder containing PO output CSVs.

    Returns:
        list: List of absolute filepaths (str) of all detected CSVs

    """

    csv_filepaths = []

    for file in os.listdir(input_dir):
        if '_po.csv' in file.lower():
            csv_filepaths.append(os.path.join(input_dir, file))
    return csv_filepaths


def parse_po_csv(input_file: str) -> tuple[pd.DataFrame, str]:
    """
    This function reads a PO line csv and returns a cleaned up
    Pandas Dataframe for processing.

    Args:
        input_file: Path to PO file CSV.

    Returns:
        A tuple of two elements:
            Pandas DataFrame with cleaned data from csv.
            The name of the csv file representing the run ID.
    """
    # Run ID read by input filename prepared by TUFLOW.
    run_id = os.path.basename(input_file)

    df = pd.read_csv(input_file)

    # Drop first column with the filename
    first_column = df.columns[0]
    df.drop(first_column, axis=1, inplace=True)

    # Set index as time increment
    df.set_index(df.columns[0], inplace=True)

    return df, run_id


def parse_run_id(run_id: str) -> tuple[str, str, str]:
    run_id_l = run_id.lower()

    storm = re.search(r"\d{2,4}[.]?\d?y", run_id_l).group()
    duration = re.search(r"\d{2,4}m", run_id_l).group()
    temp_patt = re.search(r"tp\d*", run_id_l).group()

    return storm, duration, temp_patt


def get_po_lines(po_df):
    po_lines = []

    for column, values in po_df.items():
        if 'Flow' in column:
            po_lines.append(po_df[column][0])

    return po_lines


def get_max_flows(po_df: pd.DataFrame, run_id: str) -> pd.Series:
    """
    This function processes cleaned dataframe containing PO line data and returns a pd.Series
    object containing run configuration and maximum flow in each PO line for that run.

    Args:
        po_df: Pandas DataFrame containing cleaned csv data.
        run_id: The TUFLOW run ID of the csv file.

    Returns:
        pd.Series: A pandas series containing the maximum flows for all PO lines in the run.
    """

    po_lines = get_po_lines(po_df)

    po_lines_columns = [f"Max Flow {s}" for s in po_lines]

    columns = ['Run ID', 'Event', 'Duration', 'Temporal Pattern'] + po_lines_columns

    po_max_flows = []

    for column, values in po_df.items():
        if 'Flow' in column:
            # Get max flow in pd Series, ignoring text (typically PO line title)
            po_max_flows.append((pandas.to_numeric(po_df[column],
                                                   errors='coerce').max()))

    run_id_values = list(parse_run_id(run_id))
    new_row = [run_id] + run_id_values + po_max_flows

    return pd.Series(new_row, index=columns)


def concat_po_dfs(po_dfs) -> pd.DataFrame:
    all_runs = pd.DataFrame()

    for po_df in po_dfs:
        all_runs = pd.concat([all_runs, po_df])

    return all_runs.T


def main(input):
    po_csvs = get_po_csvs(input)

    all_runs_df = pd.DataFrame()

    for file in po_csvs:
        df, run_id = parse_po_csv(file)
        new_row = get_max_flows(df, run_id)
        all_runs_df = pd.concat([all_runs_df, new_row], axis=1)
    return all_runs_df.T


def get_critical_storm(all_runs_df: pd.DataFrame):

    df = all_runs_df
    events = all_runs_df['Event'].unique()
    durations = all_runs_df['Duration'].unique()
    temp_patts = all_runs_df['Temporal Pattern'].unique()

    key =
    for column in df.items():
        if

    print(df[df['Duration'] == '120m'])

all_runs = main(input_dir)
get_critical_storm(all_runs)