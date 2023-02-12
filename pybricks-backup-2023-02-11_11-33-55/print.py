
def print_motor_settings(motor):
    print("+++++ Motor settings +++++")
    print(f"Motor settings (max_voltage [mV]): {motor.settings()}")
    print(f"Motor control limits (speed [deg/s], acceleration [deg/s^2], torque [mNm]): {motor.control.limits()}")
    print("")

################################################################################
# Used for single motor test

def print_measurements_format_type_1():
    print("+++++ Format measurements - start +++++")
    print("Duty cycle [%]")
    print("Hub battery voltage [mV]")
    print("Hub battery supplied current [mA]")
    print("Motor speed: [deg/s]")
    print("Motor load: [mNm]")
    print("Time [ms]")
    print("+++++ Format measurements - end +++++")
    print("")

def print_measurements_type_1(duty, hub, motor, watch):
    print(f"{duty};{hub.battery.voltage()};{hub.battery.current()};{motor.speed()};{motor.load()};{watch.time()}")

################################################################################
# Used for hub only test

def print_measurements_format_type_2():
    print("+++++ Format measurements - start +++++")
    print("Hub battery voltage [mV]")
    print("Hub battery supplied current [mA]")
    print("Time [ms]")
    print("+++++ Format measurements - end +++++")
    print("")

def print_measurements_type_2(hub, watch):
    print(f"{hub.battery.voltage()};{hub.battery.current()};{watch.time()}")


