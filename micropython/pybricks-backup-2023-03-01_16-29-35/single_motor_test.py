from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
from usys import stdout

hub = InventorHub()

motor = Motor(Port.A)
motor.reset_angle(angle=0.0)


# Definitions for the test program:
time_between_steps = 1000    # Target time between steps
time_between_logs = 2     # Target time between loggings
logs_between_steps = int(time_between_steps/time_between_logs)
duties = [0, 30, 100, 0, -50, 50]
duty = []
for number in duties:
    duty.extend([number]*logs_between_steps)
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
    #Consider extending them all into single list
    motor.dc(duty=duty[i])
    mem_hub_battery_voltage[i] = hub.battery.voltage()
    mem_hub_battery_current[i] = hub.battery.current()
    mem_motor_speed[i] = motor.speed()
    mem_motor_load[i] = motor.load()
    mem_time[i] = watch.time()
    wait(time=time_between_logs)
motor.stop()  

# Sending header
stdout.buffer.write(bytearray("Start,"))
stdout.buffer.write(bytearray(
    "Duty cycle [%],"
    "Hub battery voltage [mV],"
    "Hub battery supplied current [mA],"
    "Motor speed [deg/s]," 
    "Motor load [mNm],"  
    "Time [ms]"             
))
stdout.buffer.write(bytearray("Header-To-Data;"))

#Sending data
for i in range(len_duty): 
    pt1 = duty[i]
    pt2 = mem_hub_battery_voltage[i]
    pt3 = mem_hub_battery_current[i]
    pt4 = mem_motor_speed[i]
    pt5 = mem_motor_load[i]
    pt6 = mem_time[i]
    string = f"{pt1},{pt2},{pt3},{pt4},{pt5},{pt6};"
    stdout.buffer.write(bytearray(string))
stdout.buffer.write(bytearray("Done"))