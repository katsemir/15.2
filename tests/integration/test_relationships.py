import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CONF = BASE / "conf"


def _extract_declared_items() -> set[str]:
    text = (CONF / "items" / "smart_home.items").read_text(encoding="utf-8")
    names: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        parts = line.split()
        if len(parts) > 1 and parts[0] != "Group":
            names.add(parts[1])
    return names


def test_sitemap_items_exist_in_items_file() -> None:
    declared = _extract_declared_items()
    sitemap = (CONF / "sitemaps" / "dashboard.sitemap").read_text(encoding="utf-8")
    used = set(re.findall(r"item=([A-Za-z0-9_]+)", sitemap))
    assert used <= declared


def test_thing_channels_cover_automation_need() -> None:
    things = (CONF / "things" / "devices.things").read_text(encoding="utf-8")
    assert "temperature" in things
    assert "pump" in things


def test_sample_json_payload_is_valid() -> None:
    import json

    payload = (CONF / "yaml" / "simulation.json").read_text(encoding="utf-8")
    data = json.loads(payload)
    assert data["device"] == "greenhouse-controller"
    assert "metrics" in data
