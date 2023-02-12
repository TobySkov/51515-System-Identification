from tests_helper_functions import *


fig = visalize_multiple_dataframes(
    title="Motors step reponse tests",
    subtitles=["Motor 1 test", "Motor 2 test", "Motor 3 test", "Motor 4 test"],
    data=[
        load_and_format_data(file_name="motor_1_program_1.txt"),
        load_and_format_data(file_name="motor_2_program_1.txt"),
        load_and_format_data(file_name="motor_3_program_1.txt"),
        load_and_format_data(file_name="motor_4_program_1.txt")
    ]
)

fig.write_html("tests/all_motors.html")


fig = visualize_data(
    title = "Hub only, no motors",
    data = load_and_format_data(file_name="hub_only.txt"),
    )


fig.write_html("tests/only_hub.html")



