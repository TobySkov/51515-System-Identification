import os
import pandas as pd
from pathlib import Path
from paths import test_figures_folder, test_results_folder

pd.options.plotting.backend = "plotly"

data = pd.read_pickle(test_results_folder.joinpath('2023_03_03_Motor_1_Program_1.pkl'))

fig = data.plot(x='Time [ms]', y=data.columns)
fig.write_html(test_figures_folder.joinpath("2023_03_03_Motor_1_Program_1.html"))


