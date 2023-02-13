"""Helper functions for handling file loading, formatting, visualizations and analysis"""
import os.path
import pandas as pd
from pathlib import Path
import numpy as np
from typing import Tuple, List
pd.options.plotting.backend = "plotly"
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def load_and_format_data(file_name: str) -> pd.DataFrame:
    """Loading and formatting data from tests"""

    file = Path(__file__).parents[1].joinpath(f"test_results/{file_name}")
    if not os.path.exists(file):
        raise Exception(f"File does not exists: {file.__str__()}")
    
    with open(file, "r") as infile:
        lines = infile.readlines()

    data = []
    columns = []
    read_data = False
    k = 1
    for i, line in enumerate(lines):

        # Reading data format description
        if "Format measurements - start" in line:
            print("Reading measurements format...", end="")
            while "Format measurements - end" not in lines[i+k]:
                columns.append(lines[i+k].replace("\n", ""))
                k += 1
            print("Done")

        # Reading csv line
        if read_data:
            data.append([float(x) for x in line.replace(";\n","").split(";")])

        # Triggering reading data
        if "Data log" in line:
            print("Reading csv data...", end="")
            read_data = True
    print("Done")
    return pd.DataFrame.from_records(data=data, columns=columns, index="Time [ms]")


def visualize_data(title: str, data: pd.DataFrame):
    fig = data.plot.line(title=title, markers=True)
    return fig


def visalize_multiple_dataframes(title: str, subtitles: List[str], data: List[pd.DataFrame]):
    
    # Checking that columns and index are identical
    for i in range(len(data)-1):
        assert data[0].index.name == data[i+1].index.name, 'Index in all data frame must be identical'
        assert np.all(data[0].columns == data[i+1].columns), 'Columns in all data frame must be identical'


    fig = go.Figure()

    for i, column in enumerate(data[0].columns):
        for j, dataframe in enumerate(data):
            fig.add_trace(
                go.Scatter(name=f"{subtitles[j]} - {column}", x=dataframe.index, y=dataframe[column], mode="lines+markers"),
            )

    fig.update_layout(title_text=title,
    xaxis_title=data[0].index.name)

    return fig

def select_data_subset(data: pd.DataFrame, index: list) -> pd.DataFrame:
    assert len(index)==2
    subset_bool = np.logical_and(data.index >= index[0], data.index <= index[1])
    return data[subset_bool]


def estimate_average_voltage_and_current(data: pd.DataFrame) -> Tuple[float, float]:
    return (
        data["Hub battery supplied current [mA]"].mean(),
        data["Hub battery voltage [mV]"].mean()
    )


def rpm_to_rad_per_s(rpm: np.ndarray):
    assert isinstance(rpm, np.ndarray)

    rad_per_s = np.zeros(len(rpm))

    for i, number in enumerate(rpm):
        rad_per_s[i] = ((2*np.pi)/60.0)*number

    return rad_per_s






