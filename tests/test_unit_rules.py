from dataclasses import dataclass


@dataclass
class MockItem:
    name: str
    state: object = None

    def sendCommand(self, value):
        self.state = value


def rule_turn_light_on_when_door_opens(door_state, light_item):
    if door_state == "OPEN":
        light_item.sendCommand("ON")
        return "ON"
    return light_item.state


def rule_high_temperature_alert(temp_value):
    if temp_value is None:
        return "INVALID"

    if temp_value > 28:
        return "HIGH_TEMP"

    if temp_value < -20:
        return "SENSOR_ERROR"

    return "NORMAL"


def test_rule_turns_light_on_when_door_opens():
    light = MockItem(name="LivingRoom_Light", state="OFF")
    result = rule_turn_light_on_when_door_opens("OPEN", light)

    assert result == "ON"
    assert light.state == "ON"


def test_rule_does_not_change_light_when_door_closed():
    light = MockItem(name="LivingRoom_Light", state="OFF")
    result = rule_turn_light_on_when_door_opens("CLOSED", light)

    assert result == "OFF"
    assert light.state == "OFF"


def test_high_temperature_alert_detected():
    result = rule_high_temperature_alert(31.5)
    assert result == "HIGH_TEMP"


def test_normal_temperature_state():
    result = rule_high_temperature_alert(23.0)
    assert result == "NORMAL"


def test_temperature_none_edge_case():
    result = rule_high_temperature_alert(None)
    assert result == "INVALID"


def test_temperature_sensor_error_edge_case():
    result = rule_high_temperature_alert(-50)
    assert result == "SENSOR_ERROR"