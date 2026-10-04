"""Write the English/German entity name table into README.md.

Run with: PYTHONPATH=. uv run python scripts/entity_table.py
"""

import json
from pathlib import Path

import homeassistant
from homeassistant.util import slugify

from custom_components.solakon_one.binary_sensor import (
    BINARY_SENSOR_ENTITY_DESCRIPTIONS,
)
from custom_components.solakon_one.number import NUMBER_ENTITY_DESCRIPTIONS
from custom_components.solakon_one.select import SELECT_ENTITY_DESCRIPTIONS
from custom_components.solakon_one.sensor import SENSOR_ENTITY_DESCRIPTIONS

ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS = ROOT / "custom_components" / "solakon_one" / "translations"
HA_COMPONENTS = Path(homeassistant.__file__).parent / "components"
README = ROOT / "README.md"
DEVICE_NAME = "Solakon ONE"
LANGUAGES = ("en", "de")
START = "<!-- entity-table:start -->"
END = "<!-- entity-table:end -->"
PLATFORMS = {
    "binary_sensor": BINARY_SENSOR_ENTITY_DESCRIPTIONS,
    "number": NUMBER_ENTITY_DESCRIPTIONS,
    "select": SELECT_ENTITY_DESCRIPTIONS,
    "sensor": SENSOR_ENTITY_DESCRIPTIONS,
}


def load(path: Path) -> dict:
    """Read a translation file."""
    return json.loads(path.read_text())


def entity_name(platform: str, description, lang: str) -> str:
    """Entity name as Home Assistant builds it from translation key or device class."""
    own = load(TRANSLATIONS / f"{lang}.json")["entity"].get(platform, {})
    key = description.translation_key or description.key
    if key in own:
        placeholders = description.translation_placeholders or {}
        return own[key]["name"].format(**placeholders)
    ha = load(HA_COMPONENTS / platform / "translations" / f"{lang}.json")
    return ha["entity_component"][description.device_class]["name"]


def entity_id(platform: str, name: str) -> str:
    """Entity ID Home Assistant derives from the device and entity name."""
    return f"{platform}.{slugify(f'{DEVICE_NAME} {name}')}"


def build_table() -> str:
    """Markdown table with key, English and German entity ID for every entity."""
    rows = [
        "| Platform | Key | English entity ID | German entity ID |",
        "|---|---|---|---|",
    ]
    for platform, descriptions in PLATFORMS.items():
        for description in sorted(descriptions, key=lambda d: d.key):
            ids = [
                entity_id(platform, entity_name(platform, description, lang))
                for lang in LANGUAGES
            ]
            rows.append(
                f"| {platform} | `{description.key}` | "
                + " | ".join(f"`{i}`" for i in ids)
                + " |"
            )
    return "\n".join(rows)


def main() -> None:
    """Replace the table between the markers in README.md."""
    text = README.read_text()
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(f"{head}{START}\n{build_table()}\n{END}{tail}")


if __name__ == "__main__":
    main()
