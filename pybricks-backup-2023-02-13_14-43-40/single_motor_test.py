from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch

hub = InventorHub()

motor = Motor(Port.A)
motor.reset_angle(angle=0.0)

print("++++++++++++++++++++++++++++ Header +++++++++++++++++++++++++++++++++++")
print("+++++ Experiment info +++++")
print("\n\n\n")
print("+++++ Motor settings +++++")
print(f"Motor settings (max_voltage [mV]): {motor.settings()}")
print(f"Motor control limits (speed [deg/s], acceleration [deg/s^2], torque [mNm]): {motor.control.limits()}")
print("")
print("+++++ Format measurements - start +++++")
print("Duty cycle [%]")
print("Hub battery voltage [mV]")
print("Hub battery supplied current [mA]")
print("Motor speed: [deg/s]")
print("Motor load: [mNm]")
print("Time [ms]")
print("+++++ Format measurements - end +++++")
print("")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# Definitions for the test program:
time_between_steps = 1000    # Target time between steps
time_between_logs = 5     # Target time between loggings
logs_between_steps = int(time_between_steps/time_between_logs)
duty = [0]*logs_between_steps+[30]*logs_between_steps+[100]*logs_between_steps
len_duty = len(duty)

# Allocate memory:
mem_hub_battery_voltage = [0]*len_duty 
mem_hub_battery_current = [0]*len_duty
mem_motor_speed = [0]*len_duty
mem_motor_load = [0]*len_duty
mem_time = [0]*len_duty

# Initialize variables:
watch = StopWatch()

# Run tests:
for i in range(len_duty):
    motor.dc(duty=duty[i])
    mem_hub_battery_voltage[i] = hub.battery.voltage()
    mem_hub_battery_current[i] = hub.battery.current()
    mem_motor_speed[i] = motor.speed()
    mem_motor_load[i] = motor.load()
    mem_time[i] = watch.time()
    wait(time=time_between_logs)

motor.stop()  

# Output results:
print("+++++ Data log +++++")
for i in range(len_duty):

    part1 = f"{duty[i]};"
    part2 = f"{mem_hub_battery_voltage[i]};"
    part3 = f"{mem_hub_battery_current[i]};"
    part4 = f"{mem_motor_speed[i]};"
    part5 = f"{mem_motor_load[i]};"
    part6 = f"{mem_time[i]};"

    print(part1+part2+part3+part4+part5+part6)


