from pybricks.hubs import InventorHub
from pybricks.tools import wait, StopWatch

hub = InventorHub()

print("++++++++++++++++++++++++++++ Header +++++++++++++++++++++++++++++++++++")
print("+++++ Experiment info +++++")
print("\n\n\n")
print("+++++ Format measurements - start +++++")
print("Hub battery voltage [mV]")
print("Hub battery supplied current [mA]")
print("Time [ms]")
print("+++++ Format measurements - end +++++")
print("")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++ Data log +++++")

# Definitions for the test program:
total_loggings = 900  
target_time_between_logging = 1     

# Allocate memory:
mem_hub_battery_voltage = [0]*total_loggings
mem_hub_battery_current = [0]*total_loggings
mem_time = [0]*total_loggings

# Initialize variables:
watch = StopWatch()

# Run tests:
for i in range(total_loggings):
    mem_hub_battery_voltage[i] = hub.battery.voltage()
    mem_hub_battery_current[i] = hub.battery.current()
    mem_time[i] = watch.time()
    wait(time=target_time_between_logging)


# Output results:
print(f"Test completed")
print("+++++ Data log +++++")
for i in range(total_loggings):

    part1 = f"{mem_hub_battery_voltage[i]};"
    part2 = f"{mem_hub_battery_current[i]};"
    part3 = f"{mem_time[i]};"

    print(part1+part2+part3)

