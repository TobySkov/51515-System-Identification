
from pathlib import Path
import pandas as pd
pd.options.plotting.backend = "plotly"

data_folder = Path(__file__).parents[1].joinpath('test_results')
data = pd.read_pickle(data_folder.joinpath('2023_03_01_Motor_4.pkl'))

test_figures_folder = Path(__file__).parents[1].joinpath("test_figures")


fig = data.plot(x='Time [ms]', y=data.columns)
fig.write_html(test_figures_folder.joinpath("2023_03_01_Motor_4.html"))


