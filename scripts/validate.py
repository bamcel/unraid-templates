"""Validate the unified Unraid Community Applications repository."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("Name", "Repository", "Overview", "Project", "Support", "TemplateURL", "Icon")
RAW_PREFIX = "https://raw.githubusercontent.com/bamcel/unraid-templates/main/"


def text(root: ET.Element, field: str, source: Path) -> str:
    value = (root.findtext(field) or "").strip()
    if not value:
        raise ValueError(f"{source}: <{field}> must not be empty")
    return value


def http_url(value: str, field: str, source: Path) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{source}: <{field}> must be an absolute HTTP(S) URL")


def main() -> int:
    try:
        profile_path = ROOT / "ca_profile.xml"
        profile = ET.parse(profile_path).getroot()
        if profile.tag != "CommunityApplications":
            raise ValueError("ca_profile.xml: expected <CommunityApplications> root")
        text(profile, "Profile", profile_path)
        for field in ("Icon", "WebPage", "Forum"):
            http_url(text(profile, field, profile_path), field, profile_path)

        templates = sorted((ROOT / "templates").glob("*.xml"))
        if not templates:
            raise ValueError("templates/: at least one Docker template is required")
        names: set[str] = set()
        for source in templates:
            container = ET.parse(source).getroot()
            if container.tag != "Container" or container.attrib.get("version") != "2":
                raise ValueError(f'{source}: expected <Container version="2"> root')
            values = {field: text(container, field, source) for field in REQUIRED}
            if values["Name"] in names:
                raise ValueError(f'{source}: duplicate app name {values["Name"]}')
            names.add(values["Name"])
            for field in ("Project", "Support", "TemplateURL", "Icon"):
                http_url(values[field], field, source)
            expected = f"{RAW_PREFIX}templates/{source.name}"
            if values["TemplateURL"] != expected:
                raise ValueError(f"{source}: TemplateURL must be {expected}")
            if not values["Icon"].startswith(f"{RAW_PREFIX}icons/"):
                raise ValueError(f"{source}: Icon must be hosted in this repository's icons directory")
            icon = ROOT / values["Icon"].removeprefix(RAW_PREFIX)
            if not icon.is_file():
                raise ValueError(f"{source}: missing local icon {icon}")
    except (ET.ParseError, OSError, ValueError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1
    print(f"Validated ca_profile.xml and {len(templates)} app templates: {', '.join(sorted(names))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
