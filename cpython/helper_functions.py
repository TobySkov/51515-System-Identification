"""Helper functions for handling file loading, formatting, visualizations and analysis"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper
import plotly.graph_objects as go
from typing import Tuple, List, Union
pd.options.plotting.backend = "plotly"


def rpm_to_rad_per_s(rpm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Revolutions per minute to radians per second"""
    return ((2*np.pi)/60.0)*rpm


def deg_per_s_to_rad_per_s(deg_per_s: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Degrees per second to radians per second"""
    return (np.pi/180.0)*deg_per_s


def deg_per_s_to_rpm(deg_per_s: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Degrees per second to revolutions per minute"""
    return (60.0/360.0)*deg_per_s


def select_voltage_current_rotations_steady_state_subset(
        data: pd.DataFrame, 
        ss_timestamps: List[tuple]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Selecting steady state datasubset and calculating average values for voltage, current and rotations
    """
    V = np.zeros(len(ss_timestamps))
    I = np.zeros(len(ss_timestamps))
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


def ols_voltage_current_rotations(
        V: np.ndarray, 
        I: np.ndarray, 
        omega: np.ndarray,
) -> RegressionResultsWrapper:
    """Conducting ordinary least squares regression on equation:
    
    V = I*R + K_e*omega
    """
    X = pd.DataFrame({
        'R': I,
        'K_e': omega,
    })
    
    return sm.OLS(V, X).fit()





def estimate_hub_average_voltage_and_current(data: pd.DataFrame) -> Tuple[float, float]:
    return (
        data["Hub battery supplied current [mA]"].mean(),
        data["Hub battery voltage [mV]"].mean()
    )

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
