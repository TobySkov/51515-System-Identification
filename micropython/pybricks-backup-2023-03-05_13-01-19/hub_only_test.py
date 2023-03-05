from pybricks.hubs import InventorHub
from pybricks.tools import wait, StopWatch
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from usys import stdout

hub = InventorHub()

mem_hub_battery_voltage = [0.0]*9000
mem_hub_battery_current = [0.0]*9000
mem_time = [0.0]*9000

# Initialize variables:
watch = StopWatch()

# 3s with on attachments
k=0
for i in range(3000):
    mem_hub_battery_voltage[k] = hub.battery.voltage()
    mem_hub_battery_current[k] = hub.battery.current()
    mem_time[k] = watch.time()
    k+=1
    wait(time=1)

# 3s with registered motor
motor = Motor(Port.A)
for i in range(3000):
    mem_hub_battery_voltage[k] = hub.battery.voltage()
    mem_hub_battery_current[k] = hub.battery.current()
    mem_time[k] = watch.time()
    k+=1
    wait(time=1)

# 3s with motor at zero duty
motor.dc(duty=0)
for i in range(3000):
    mem_hub_battery_voltage[k] = hub.battery.voltage()
    mem_hub_battery_current[k] = hub.battery.current()
    mem_time[k] = watch.time()
    k+=1
    wait(time=1)
motor.stop()  


# Sending header
stdout.buffer.write(bytearray("Start,"))
stdout.buffer.write(bytearray(
    "Hub battery voltage [mV],"
    "Hub battery supplied current [mA],"
    "Time [ms]"             
))
stdout.buffer.write(bytearray("Header-To-Data;"))

#Sending data
for i in range(9000): 
    pt1 = mem_hub_battery_voltage[i]
    pt2 = mem_hub_battery_current[i]
    pt3 = mem_time[i]
    string = f"{pt1},{pt2},{pt3};"
    stdout.buffer.write(bytearray(string))
stdout.buffer.write(bytearray("Done"))