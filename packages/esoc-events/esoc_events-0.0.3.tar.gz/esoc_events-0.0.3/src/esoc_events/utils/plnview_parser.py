from typing import Any

from esoc_events.utils.xml import xml_to_obj

from .abstract_parser import AbstractParser


class PlnViewParser(AbstractParser):

    def __init__(self, path: Any) -> None:
        AbstractParser.__init__(self, path)
        self._all = self.root.findall(".//service_session")
        self.reset()

    @property
    def sessions(self) -> list:
        return [
            xml_to_obj(session).get("service_session") for session in self._sessions
        ]

    def reset(self) -> Any:
        self._sessions = self._all
        return self

    def satellite(self, name: str) -> Any:
        return self.__query__(
            lambda session: session.find("./satellite_id").text == name
        )

    def after(self, isoc_utc: str) -> Any:
        return self.__query__(
            lambda session: session.find("./activity_start").text > isoc_utc
        )

    def before(self, isoc_utc: str) -> Any:
        return self.__query__(
            lambda session: session.find("./activity_end").text < isoc_utc
        )

    def ground_station(self, name: str) -> Any:
        return self.__query__(
            lambda session: session.find("./ground_station").text == name
        )

    def __query__(self, function: Any) -> Any:
        self._sessions = list(filter(function, self._sessions))
        return self
