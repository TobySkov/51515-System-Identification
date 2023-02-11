"""Helper functions for handling file loading, formatting, visualizations and analysis"""
import os.path
import pandas as pd
from pathlib import Path
import numpy as np
from typing import Tuple, List
pd.options.plotting.backend = "plotly"


def load_and_format_data(file_name: str) -> pd.DataFrame:
    """Loading and formatting data from tests"""

    file = Path(__file__).parent.joinpath(f"data/{file_name}")
    if not os.path.exists(file):
        raise Exception(f"File does not exists")
    
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
            data.append([float(x) for x in line.split(";")])

        # Triggering reading data
        if "Data log" in line:
            print("Reading csv data...", end="")
            read_data = True
    print("Done")
    return pd.DataFrame.from_records(data=data, columns=columns, index="Time [ms]")


def visualize_data(data: pd.DataFrame) -> None:
    fig = data.plot.line(markers=True)
    fig.show()


def select_data_subset(data: pd.DataFrame, index: list) -> pd.DataFrame:
    subset_bool = np.logical_and(data.index >= index[0], data.index <= index[1])
    return data[subset_bool]


def estimate_average_voltage_and_current(data: pd.DataFrame) -> Tuple[float, float]:
    return (
        data["Hub battery supplied current [mA]"].mean(),
        data["Hub battery voltage [mV]"].mean()
    )

def calc_electrical_resistance(V: List[float], I: List[float], tau: List[float], omega: List[float]) -> List[float]:
    assert len(V) == len(I) and len(V) == len(tau) and len(V) == len(omega), "Input lists must be equal length" 
    R = []
    for i in range(len(V)):
        R.append(
            V[i]/I[i] - (tau[i]*omega[i])/(I[i]*I[i])
        )

    return R

if __name__ == "__main__":
    data = load_and_format_data("motor_test_04_02_2023__no1.txt")
    visualize_data(data)
    data = select_data_subset(data, [0,1950])
    visualize_data(data)
    I,V = estimate_average_voltage_and_current(data)
    print(f"Estimated current: {np.round(I,3)} [mA];\tEstimated voltage: {np.round(V,3)} [mA]")
    
