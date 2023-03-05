# NOTE: Run this program with the latest
# firmware provided via https://beta.pybricks.com/
from pybricks.hubs import InventorHub
from pybricks.pupdevices import ColorSensor
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.parameters import Color

hub = InventorHub()

motor = Motor(Port.A)
motor.reset_angle(angle=0.0)

sensor = ColorSensor(Port.B)

print(sensor.detectable_colors())

color = sensor.color().v

print(type(color))

#isinstance(color, Color.WHITE)

"""
motor.dc(20)

for i in range(200)

    # Read the color and reflection
    colors[i] = sensor.color()


    # Wait so we can read the value.
    wait(1)
"""
