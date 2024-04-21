from typing import Any

from esoc_events.utils.time import fdyn_to_iso

from .abstract_parser import AbstractParser


class EvtcParser(AbstractParser):

    def __init__(self, path: Any) -> None:
        AbstractParser.__init__(self, path)
        self.ns_map = {"ns": "http://esa.esoc.events", "ems": "http://esa.esoc.ems"}
        self._all = self.root.findall(".//ns:events/*", self.ns_map)
        self.reset()

    @property
    def events(self) -> list:
        return self._events

    def reset(self) -> Any:
        self._events = self._all
        return self

    def id(self, name: str) -> Any:
        return self.__query__(lambda event: event.get("id") == name)

    def ids(self, names: list) -> Any:
        return self.__query__(lambda event: event.get("id") in names)

    def count(self, count: int) -> Any:
        return self.__query__(lambda event: int(event.get("count")) == count)

    def counts(self, counts: list) -> Any:
        return self.__query__(lambda event: int(event.get("count")) in counts)

    def after(self, isoc_utc: str) -> Any:
        return self.__query__(lambda event: fdyn_to_iso(event.get("time")) > isoc_utc)

    def before(self, isoc_utc: str) -> Any:
        return self.__query__(lambda event: fdyn_to_iso(event.get("time")) < isoc_utc)

    def __query__(self, function: Any) -> Any:
        self._events = list(filter(function, self._events))
        return self

    def query_item(self, id_str: str, count: str) -> Any:
        for event in self._all:
            if (event.get("id") == id_str) and (event.get("count") == count):
                return event
        return None
