from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from usys import stdout

hub = InventorHub()

motor = Motor(Port.A)
motor.reset_angle(angle=0.0)

sensor = ColorSensor(Port.B)

# Definitions for the test program:
measurement_interval = 6000         # Target time between steps [ms]
time_between_logs = 2               # Target time between loggings
logs_during_interval = int(measurement_interval/time_between_logs)

# Program:
duty = 30
file_name = f"2023_03_05_Motor_1_with_colorsensor_Step_{duty}"

# Allocate memory:
mem_duty = [0.0]*logs_during_interval
mem_hub_battery_voltage = [0.0]*logs_during_interval
mem_hub_battery_current = [0.0]*logs_during_interval
mem_motor_speed = [0.0]*logs_during_interval
mem_motor_load = [0.0]*logs_during_interval
mem_color = [0.0]*logs_during_interval
mem_time = [0.0]*logs_during_interval


# Initialize motor dc function, as if the motor was operating already
motor.dc(0)
wait(1000)

# Initialize variables:
watch = StopWatch()

motor.dc(duty=duty)
for i in range(logs_during_interval):
    mem_duty[i] = duty
    mem_hub_battery_voltage[i] = hub.battery.voltage()
    mem_hub_battery_current[i] = hub.battery.current()
    mem_motor_speed[i] = motor.speed()
    mem_motor_load[i] = motor.load()
    mem_color[i] = sensor.color().v
    mem_time[i] = watch.time()
    wait(time=time_between_logs)
motor.stop()


# Sending header
stdout.buffer.write(bytearray(f"Name:{file_name},"))
stdout.buffer.write(bytearray(
    "Duty cycle [%],"
    "Hub battery voltage [mV],"
    "Hub battery supplied current [mA],"
    "Motor speed [deg/s]," 
    "Motor load [mNm],"  
    "Color brightness [%],"
    "Time [ms];"             
))
stdout.buffer.write(bytearray("Header-To-Data;"))

#Sending data
for i in range(logs_during_interval): 
    pt1 = mem_duty[i]
    pt2 = mem_hub_battery_voltage[i]
    pt3 = mem_hub_battery_current[i]
    pt4 = mem_motor_speed[i]
    pt5 = mem_motor_load[i]
    pt6 = mem_color[i]
    pt7 = mem_time[i]
    string = f"{pt1},{pt2},{pt3},{pt4},{pt5},{pt6},{pt7};"
    stdout.buffer.write(bytearray(string))
stdout.buffer.write(bytearray("Done"))



