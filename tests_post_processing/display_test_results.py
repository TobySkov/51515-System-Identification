from tests_helper_functions import *
from pathlib import Path

test_figures_folder = Path(__file__).parents[1].joinpath("test_figures")

fig = visalize_multiple_dataframes(
    title="Motors step reponse tests",
    subtitles=["Motor 1 test", "Motor 2 test", "Motor 3 test", "Motor 4 test"],
    data=[
        load_and_format_data(file_name="motor_1__2023_02_13.txt"),
        load_and_format_data(file_name="motor_2__2023_02_13.txt"),
        load_and_format_data(file_name="motor_3__2023_02_13.txt"),
        load_and_format_data(file_name="motor_4__2023_02_13.txt")
    ]
)

fig.write_html(test_figures_folder.joinpath("all_motors__2023_02_13.html"))


fig = visualize_data(
    title = "Hub only, no motors",
    data = load_and_format_data(file_name="hub_only__2023_02_13.txt"),
    )


fig.write_html(test_figures_folder.joinpath("hub_only__2023_02_13.html"))



