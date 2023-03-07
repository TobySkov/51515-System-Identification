
import pandas as pd
pd.options.plotting.backend = "plotly"
from paths import test_results_folder
from helper_functions import *

data = pd.read_pickle(test_results_folder.joinpath('2023_03_05_Motor_1_with_colorsensor_Step_30.pkl'))
fig = data.plot(x='Time [ms]', y=data.columns, markers=True)
fig.show()

ss_start_time = 700



# Function start
ss_subset = data['Time [ms]'] > ss_start_time

ss_data = data[ss_subset]
ss_data.reset_index(inplace=True, drop=True)


cycles = []
cycle = []
for i in range(len(ss_data) - 1):

    if ss_data.at[i, 'Color brightness [%]'] != ss_data.at[i+1, 'Color brightness [%]']:
            cycle.append(ss_data.at[i, 'Time [ms]'])

    if len(cycle) == 3:
            cycles.append(cycle)
            start_new_cycle = cycle[2]
            cycle = [start_new_cycle]

print(f"Identified cycles (start, mid, end) [ms]: {cycles}")

deg_per_s = []
for cycle in cycles:
    ms_per_round = cycle[2] - cycle[0]
    deg_per_s.append(ms_per_round_to_deg_per_s(ms_per_round))


# Steady state data with full cycles colorsensor (cs) measurements:
ss_cs_data = ss_data[
      (cycles[0][0] < ss_data['Time [ms]']) & (ss_data['Time [ms]'] <= cycles[-1][2])
]


color_sensor_motor_speed = np.zeros(len(ss_cs_data))
average_motor_speed = np.zeros(len(ss_cs_data))

for i, cycle in enumerate(cycles):
    selector = (cycle[0] < ss_cs_data['Time [ms]']) & (ss_cs_data['Time [ms]'] <= cycle[2])

    color_sensor_motor_speed[selector] = deg_per_s[i]
    average_motor_speed[selector] = ss_cs_data['Motor speed [deg/s]'].values[selector].mean()

ss_cs_data['Motor speed - colorsensor [deg/s]'] = color_sensor_motor_speed
ss_cs_data['Motor speed - average measured during cycle [deg/s]'] = average_motor_speed

fig = ss_cs_data.plot(x='Time [ms]', y=ss_cs_data.columns, markers=True)
fig.show()





