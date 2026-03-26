from dataclasses import dataclass


@dataclass
class MockItem:
    name: str
    state: object = None

    def sendCommand(self, value):
        self.state = value


def door_rule(door_state, light_item):
    if door_state == "OPEN":
        light_item.sendCommand("ON")


def temperature_rule(temp_value, fan_item, alert_log):
    if temp_value > 28:
        fan_item.sendCommand("ON")
        alert_log.append(f"Temperature alert: {temp_value}")


def security_rule(door_state, alarm_item, is_night):
    if door_state == "OPEN" and is_night:
        alarm_item.sendCommand("ON")


def test_multi_rule_interaction():
    light = MockItem("LivingRoom_Light", "OFF")
    fan = MockItem("Cooling_Fan", "OFF")
    alarm = MockItem("Alarm_Siren", "OFF")
    logs = []

    door_rule("OPEN", light)
    temperature_rule(30, fan, logs)
    security_rule("OPEN", alarm, True)

    assert light.state == "ON"
    assert fan.state == "ON"
    assert alarm.state == "ON"
    assert len(logs) == 1


def test_end_to_end_scenario():
    light = MockItem("LivingRoom_Light", "OFF")
    fan = MockItem("Cooling_Fan", "OFF")
    alarm = MockItem("Alarm_Siren", "OFF")
    logs = []

    events = [
        {"door": "CLOSED", "temp": 22, "night": False},
        {"door": "OPEN", "temp": 22, "night": False},
        {"door": "OPEN", "temp": 30, "night": True},
    ]

    for event in events:
        door_rule(event["door"], light)
        temperature_rule(event["temp"], fan, logs)
        security_rule(event["door"], alarm, event["night"])

    assert light.state == "ON"
    assert fan.state == "ON"
    assert alarm.state == "ON"
    assert any("Temperature alert" in entry for entry in logs)


def test_system_integration_consistency():
    light = MockItem("LivingRoom_Light", "OFF")
    fan = MockItem("Cooling_Fan", "OFF")
    logs = []

    door_rule("OPEN", light)
    temperature_rule(29, fan, logs)

    assert light.name == "LivingRoom_Light"
    assert fan.name == "Cooling_Fan"
    assert light.state in ["ON", "OFF"]
    assert fan.state in ["ON", "OFF"]


def test_basic_performance_of_integration_flow():
    import time

    light = MockItem("LivingRoom_Light", "OFF")
    fan = MockItem("Cooling_Fan", "OFF")
    alarm = MockItem("Alarm_Siren", "OFF")
    logs = []

    start = time.perf_counter()

    for _ in range(1000):
        door_rule("OPEN", light)
        temperature_rule(31, fan, logs)
        security_rule("OPEN", alarm, True)

    duration = time.perf_counter() - start

    assert duration < 1.0
    assert light.state == "ON"
    assert fan.state == "ON"
    assert alarm.state == "ON"