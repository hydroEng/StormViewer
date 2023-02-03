import os
import statistics
import pandas
import pandas as pd
import re

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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
    """
    This function reads the .csv filename and parses it into storm event, duration and temporal pattern respectively.

    Args:
        run_id: Name of csv file.

    Returns:
        a 3x1 tuple of strings with storm, duration and temporal pattern.

    """

    run_id_l = run_id.lower()

    storm = re.search(r"\d{2,4}[.]?\d?y", run_id_l).group()
    duration = re.search(r"\d{1,4}m", run_id_l).group()
    temp_patt = re.search(r"tp\d*", run_id_l).group()

    return storm, duration, temp_patt


def get_po_lines(po_df: pd.DataFrame) -> list[str]:
    """
    Grabs names of columns containing max flow, i.e. the po lines.
    Args:
        po_df:

    Returns:
        A list of column names containing the PO_line names
    """

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


def concat_po_dfs(po_dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """
    This function concatenates all dataframes generated from the CSV files into one dataframe. Output mimicks
    format of legacy spreadsheet.

    Args:
        po_dfs: a list of DataFrames generated from the po.csv files.

    Returns:

    """
    df = pd.DataFrame()

    for po_df in po_dfs:
        df = pd.concat([df, po_df])

    return df.T


def main(input):

    """
    What the fucc does this boi do
    Args:
        input:

    Returns:

    """
    po_csvs = get_po_csvs(input)

    all_runs_df = pd.DataFrame()

    for file in po_csvs:
        df, run_id = parse_po_csv(file)
        new_row = get_max_flows(df, run_id)
        all_runs_df = pd.concat([all_runs_df, new_row], axis=1)
    return all_runs_df.T


def split_po_dfs(df: pd.DataFrame) -> list[pd.DataFrame]:
    """
    This function takes a dataframe with multiple PO lines and splits the dataframes according to each po line for
    better manipulation.

    Args:
        df: DataFrame containing data for multiple PO lines.

    Returns:
        a list containing a DataFrame for each po_line.

    """

    po_lines = []
    po_line_dfs = []

    for column, values in df.items():
        if 'Max Flow' in column:
            po_lines.append(column)

    for po_line in po_lines:
        split_df = df
        excluded_columns = [x for x in po_lines if x != po_line]
        po_line_dfs.append(split_df.drop(columns=excluded_columns))

    return po_line_dfs


def split_event(df: pd.DataFrame) -> list[pd.DataFrame]:
    """
    This function takes a dataframe with multiple events and splits the dataframes according to each event for better
    manipulation.

    Args:
        df: DataFrame containing data for multiple events

    Returns:
        a list containing a DataFrame for each po_line
    """

    unique_events = df['Event'].unique().tolist()

    event_dfs = []

    for event in unique_events:
        event_dfs.append(df[df['Event'] == event])

    return event_dfs


def dropsort_duration(df: pd.DataFrame) -> pd.DataFrame:
    sorted_df = df
    """
    This function drops all non-numeric chars from the index ('Duration') column in dataframe and sorts the dataframe by 
    numeric value.

    Args:
        df: DataFrame with 'Duration' column.

    Returns:
        a DataFrame sorted by duration (numeric value only).

    """

    # Remove alphabetical chars from minutes
    sorted_df.index = sorted_df.index.map(lambda x: (re.sub(r"[a-zA-Z]", "", str(x))))
    sorted_df.index = sorted_df.index.map(lambda x: int(x))
    sorted_df = sorted_df.sort_index()
    return sorted_df


def get_col_name(value, input_row):
    """ Get column name of value in row generated by df.apply() method."""

    col_name = input_row[input_row == value].index[0]
    return col_name


def get_crit_tp(row: pd.Series) -> str:
    median = row['Median']

    diffs = {}
    for cell in row:
        col_name = get_col_name(cell, row)
        if 'tp' in col_name:
            diffs[col_name] = (cell - median)

    positive_diffs = {k: v for k, v in diffs.items() if v > 0}
    crit_tp = min(positive_diffs, key=positive_diffs.get)

    return crit_tp


def tp_vs_max_flow_df(df: pd.DataFrame) -> tuple[str, str, pd.DataFrame]:
    """
    This function takes a df filtered by one event and one po_line and generates a 3x1 tuple with the event, the name of
    the po_line and a dataframe presenting storm duration (x) vs temporal patterns (y), as well as average, median and
    critical temporal patterns for the run.

    Note that po_line name will be lost in this process!

    Args:
        df: DataFrame with data for one event and po_line

    Returns:
        A DataFrame sorted by duration (x) vs temporal pattern (y), avg/median values, and critical storm.
    """
    event = df['Event'].unique().tolist()[0]

    po_line: str = ""

    for column, values in df.items():
        if 'Max Flow' in column:
            po_line = str(column)

    dur_tp_df = df.pivot(index='Duration', columns='Temporal Pattern', values=po_line)
    dur_tp_df = dropsort_duration(dur_tp_df)

    tp_cols = [col for col in dur_tp_df.columns if 'tp' in col]

    dur_tp_df['Average'] = dur_tp_df[tp_cols].mean(axis=1)
    dur_tp_df['Median'] = dur_tp_df[tp_cols].median(axis=1)

    dur_tp_df['Critical TP'] = dur_tp_df.apply(get_crit_tp, axis=1)

    return event, po_line, dur_tp_df


def critical_storms(all_runs_df: pd.DataFrame):
    df = all_runs_df

    events = all_runs_df['Event'].unique()
    durations = all_runs_df['Duration'].unique()
    temp_patts = all_runs_df['Temporal Pattern'].unique()

    po_lines_dfs = split_po_dfs(all_runs_df)

    working_dfs = []

    for _ in po_lines_dfs:
        final_dfs = split_event(_)
        working_dfs.append(final_dfs)
    cleaned = []
    for x in working_dfs:
        for y in x:
            event, po_line, df = tp_vs_max_flow_df(y)
            cleaned.append(dropsort_duration(df))
    return cleaned


input_dir = r"/home/Taha/tuflow_ensemble/C01/"

all_runs = main(input_dir)
# print(all_runs)
df2 = critical_storms(all_runs)[0]

print(df2)
