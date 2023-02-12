from pybricks.hubs import InventorHub
from pybricks.tools import wait, StopWatch
from print import print_motor_settings, \
    print_measurements_format_type_2, print_measurements_type_2

hub = InventorHub()

print("++++++++++++++++++++++++++++ Header +++++++++++++++++++++++++++++++++++")
print("+++++ Experiment info +++++")
print("\n\n\n")
print_measurements_format_type_2()
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++ Data log +++++")


total_measurement_time = 9000 # 9 s
time_between_measurements = 10 # [ms]


no_of_measurements = total_measurement_time/time_between_measurements

watch = StopWatch()


for i in range(no_of_measurements):

    print_measurements_type_2(hub, watch)
    wait(time=time_between_measurements)




