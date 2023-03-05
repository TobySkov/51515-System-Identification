import os
import pandas as pd
from pathlib import Path
from paths import test_figures_folder, test_results_folder

pd.options.plotting.backend = "plotly"


for file in os.listdir(test_results_folder):

    data = pd.read_pickle(test_results_folder.joinpath(file))

    fig = data.plot(x='Time [ms]', y=data.columns, markers=True)

    fig.write_html(test_figures_folder.joinpath(file.replace('.pkl', '.html')))


