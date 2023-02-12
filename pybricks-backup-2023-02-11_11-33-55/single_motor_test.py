from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
from print import print_motor_settings, \
    print_measurements_format_type_1, print_measurements_type_1

hub = InventorHub()

motor = Motor(Port.A)
motor.reset_angle(angle=0.0)

print("++++++++++++++++++++++++++++ Header +++++++++++++++++++++++++++++++++++")
print("+++++ Experiment info +++++")
print("\n\n\n")
print_motor_settings(motor)
print_measurements_format_type_1()
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++ Data log +++++")

# Step settings

#Program 1:
steps = [30,100,100]
time_between_steps = 3000
total_time = (len(steps)) * time_between_steps
target_time = time_between_steps

k = 0
duty = 0
watch = StopWatch()
start = watch.time()

while(watch.time()-start <= total_time):

    if (watch.time()-start >= target_time):
        duty = steps[k]
        motor.dc(duty=duty)
        k += 1
        target_time += time_between_steps

    print_measurements_type_1(duty, hub, motor, watch)
    wait(time=10)

