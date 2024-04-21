import datetime
import xml.etree.ElementTree as ETree


class Uevt:

    def __init__(self, start: str, end: str) -> None:
        self.root = ETree.Element("eventfile")
        header_attrib = {
            "format_version": "1",
            "gen_time": datetime.datetime.now().isoformat()[:19] + "Z",
            "icd_version": "PLID-1.0",
            "spacecraft": "JUIC",
            "validity_start": start,
            "validity_end": end,
        }
        self.header = ETree.SubElement(self.root, "header", header_attrib)
        self.events = ETree.SubElement(self.root, "events")

    def add_event(self, id_str: str, count: str, time: str, duration: str) -> None:
        """Adds a new event to the UEVT file

        Args:
            id_str (str): event identifier
            count (str): counter
            time (str): event utc timestamp in ISOC format (YYYY-MM-DD/YYYY-DDD)
            duration (str): duration in seconds
        """
        attrib = {"id": id_str, "count": count, "time": time, "duration": duration}
        ETree.SubElement(self.events, "uvt", attrib)

    def dump(self, filename: str) -> None:
        with open(filename, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
            f.write(
                b"""<eventfile xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://esa.esoc.events juice_event_definitions.xsd"
xmlns="http://esa.esoc.events"
xmlns:ems="http://esa.esoc.ems">\n"""
            )

            tree = ETree.ElementTree(self.header)
            ETree.indent(tree)
            tree.write(f, "utf-8")
            f.write(b"\n")
            tree = ETree.ElementTree(self.events)
            ETree.indent(tree)
            tree.write(f, "utf-8")
            f.write(b"\n")
            f.write(b"""</eventfile>""")
