from dataclasses import dataclass


@dataclass
class SimulatedDevice:
    name: str
    state: object = None

    def update(self, value):
        self.state = value


def process_motion_event(motion_sensor, light_item):
    if motion_sensor.state == "MOTION":
        light_item.update("ON")
    else:
        light_item.update("OFF")


def process_time_based_scenario(hour, heater_item, temperature):
    if hour >= 22 or hour < 6:
        if temperature < 20:
            heater_item.update("ON")
        else:
            heater_item.update("OFF")
    else:
        heater_item.update("OFF")


def process_failure_scenario(sensor_value, system_log):
    if sensor_value in [None, "ERROR", "DISCONNECTED"]:
        system_log.append("Sensor failure detected")
        return "FAILED"
    return "OK"


def test_device_simulation():
    motion_sensor = SimulatedDevice("MotionSensor", "MOTION")
    light = SimulatedDevice("HallLight", "OFF")

    process_motion_event(motion_sensor, light)

    assert light.state == "ON"


def test_event_simulation():
    motion_sensor = SimulatedDevice("MotionSensor", "NO_MOTION")
    light = SimulatedDevice("HallLight", "ON")

    process_motion_event(motion_sensor, light)

    assert light.state == "OFF"


def test_time_based_scenario():
    heater = SimulatedDevice("Heater", "OFF")

    process_time_based_scenario(hour=23, heater_item=heater, temperature=18)

    assert heater.state == "ON"


def test_failure_scenario():
    logs = []
    result = process_failure_scenario("DISCONNECTED", logs)

    assert result == "FAILED"
    assert len(logs) == 1
    assert "Sensor failure detected" in logs[0]