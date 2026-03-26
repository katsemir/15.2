from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "conf"

ITEM_TYPES = {
    "Switch",
    "Number",
    "String",
    "Contact",
    "DateTime",
    "Dimmer",
    "Rollershutter",
    "Color",
    "Player",
    "Group",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_items() -> list[str]:
    errors: list[str] = []
    for file in (CONF / "items").glob("*.items"):
        for lineno, raw in enumerate(read_text(file).splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("//"):
                continue
            token = line.split()[0]
            if token not in ITEM_TYPES:
                errors.append(f"{file}:{lineno}: unknown item type '{token}'")
    return errors


def validate_things() -> list[str]:
    errors: list[str] = []
    for file in (CONF / "things").glob("*.things"):
        text = read_text(file)
        if "Thing " not in text and "Bridge " not in text:
            errors.append(f"{file}: file does not define Thing or Bridge")
        if text.count("{") != text.count("}"):
            errors.append(f"{file}: unbalanced braces")
    return errors


def validate_sitemaps() -> list[str]:
    errors: list[str] = []
    widget_pattern = re.compile(r"^(sitemap|Frame|Text|Switch|Setpoint|Slider|Chart|Image|Group)\b")
    for file in (CONF / "sitemaps").glob("*.sitemap"):
        for lineno, raw in enumerate(read_text(file).splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("//") or line in {"{", "}"}:
                continue
            if not widget_pattern.match(line):
                errors.append(f"{file}:{lineno}: unexpected sitemap statement '{line}'")
    return errors


def validate_rules() -> list[str]:
    errors: list[str] = []
    for file in (CONF / "rules").glob("*.rules"):
        text = read_text(file)
        required = ["rule", "when", "then", "end"]
        for marker in required:
            if marker not in text:
                errors.append(f"{file}: missing keyword '{marker}'")
        rule_count = len(re.findall(r'^rule\b', text, flags=re.MULTILINE))
        end_count = len(re.findall(r'^end\b', text, flags=re.MULTILINE))
        if rule_count != end_count:
            errors.append(f"{file}: number of rule and end blocks differs")
    return errors


def validate_json() -> list[str]:
    errors: list[str] = []
    for file in CONF.rglob("*.json"):
        try:
            json.loads(read_text(file))
        except json.JSONDecodeError as exc:
            errors.append(f"{file}: invalid JSON ({exc})")
    return errors


def main() -> None:
    checks = [
        validate_items,
        validate_things,
        validate_sitemaps,
        validate_rules,
        validate_json,
    ]
    problems = [issue for check in checks for issue in check()]
    if problems:
        print("Validation failed:\n")
        for issue in problems:
            print(f"- {issue}")
        raise SystemExit(1)
    print("All OpenHAB configuration checks passed.")


if __name__ == "__main__":
    main()
