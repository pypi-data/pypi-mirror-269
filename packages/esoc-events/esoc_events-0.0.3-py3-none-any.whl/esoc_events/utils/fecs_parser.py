from typing import Any
from xml.etree import ElementTree

from esoc_events.utils.time import fdyn_to_iso, get_timedelta

from .xml import replace_parenthesis_tags


class FecsParser:
    ns_map = {"ns": "http://esa.esoc.events", "ems": "http://esa.esoc.ems"}

    def __init__(self, path: Any) -> None:
        """_summary_

        Args:
            path (Any): _description_
        """
        self.path = path
        content = replace_parenthesis_tags(path)
        self._root = ElementTree.fromstring(content)
        self.reset()

    @property
    def passes(self) -> list:
        return self._passes

    def reset(self) -> Any:
        self._passes = self._root.findall('.//ns:REF[@id="pass_info"]', self.ns_map)
        return self

    @staticmethod
    def extract_pass(element: ElementTree.Element) -> Any:
        return {
            "duration": str(get_timedelta(element.attrib["duration"])),
            "station": element.get("{http://esa.esoc.ems}station"),
            "start": fdyn_to_iso(element.get("time", "")),
            "tm_rate": int(element.get("tm_rate", "")),
        }
