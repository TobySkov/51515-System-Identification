"""Helper functions for handling file loading, formatting, visualizations and analysis"""
import os.path
import pandas as pd
from pathlib import Path
import numpy as np
from typing import Tuple, List
pd.options.plotting.backend = "plotly"
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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

def select_data_subset(data: pd.DataFrame, ss_timestamps: List[tuple]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Selecting datasubset and calculating average values
    """
    I = np.zeros(len(ss_timestamps))
    V = np.zeros(len(ss_timestamps))
    omega = np.zeros(len(ss_timestamps))
    rpm = np.zeros(len(ss_timestamps))

    assert isinstance(ss_timestamps, list)
    for i, subset in enumerate(ss_timestamps):
        assert isinstance(subset, tuple)
        assert len(subset) == 2

        select = np.logical_and(data['Time [ms]']  >= subset[0], data['Time [ms]']  <= subset[1])

        # Voltage needs be substracted voltage drop of 0.2 V
        V[i] = (data[select]['Hub battery voltage [mV]'].mean()/1000 - 0.2) * data[select]['Duty cycle [%]'].mean()/100.0
        I[i] = data[select]['Hub battery supplied current [mA]'].mean()/1000
        omega[i] = deg_per_s_to_rad_per_s(
            data[select]['Motor speed [deg/s]'].mean()
        )
        rpm[i] = deg_per_s_to_rpm(
            data[select]['Motor speed [deg/s]'].mean()
        )
        
    # Current drawn by motor needs to be found, by subtraction current drawn by PCL 
    I = I - I[0] 

    return (V, I, omega, rpm)



def estimate_average_voltage_and_current(data: pd.DataFrame) -> Tuple[float, float]:
    return (
        data["Hub battery supplied current [mA]"].mean(),
        data["Hub battery voltage [mV]"].mean()
    )


def rpm_to_rad_per_s(rpm: np.ndarray) -> np.ndarray:
    assert isinstance(rpm, np.ndarray)

    rad_per_s = np.zeros(len(rpm))

    for i, number in enumerate(rpm):
        rad_per_s[i] = ((2*np.pi)/60.0)*number

    return rad_per_s



def deg_per_s_to_rad_per_s_array(deg_per_s: np.ndarray) -> np.ndarray:
    assert isinstance(deg_per_s, np.ndarray)

    rad_per_s = np.zeros(len(deg_per_s))

    divisor = 1/180.0
    for i, number in enumerate(deg_per_s):
        rad_per_s[i] = np.pi*number*divisor 

    return rad_per_s


def deg_per_s_to_rad_per_s(deg_per_s: float) -> float:
    assert isinstance(deg_per_s, float)
    return (np.pi/180.0)*deg_per_s


def deg_per_s_to_rpm(deg_per_s: float) -> float:
    assert isinstance(deg_per_s, float)
    return (60.0/360.0)*deg_per_s


