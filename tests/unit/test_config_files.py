from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CONF = BASE / "conf"


def test_main_config_files_exist() -> None:
    assert (CONF / "items" / "smart_home.items").exists()
    assert (CONF / "rules" / "automation.rules").exists()
    assert (CONF / "things" / "devices.things").exists()
    assert (CONF / "sitemaps" / "dashboard.sitemap").exists()


def test_items_file_contains_expected_entities() -> None:
    content = (CONF / "items" / "smart_home.items").read_text(encoding="utf-8")
    assert "Group gHouse" in content
    assert "Switch Pump_Control" in content
    assert "Number Greenhouse_Temperature" in content


def test_rules_file_has_openhab_rule_structure() -> None:
    content = (CONF / "rules" / "automation.rules").read_text(encoding="utf-8")
    assert 'rule "Pump automation"' in content
    assert "when" in content
    assert "then" in content
    assert content.strip().endswith("end")
