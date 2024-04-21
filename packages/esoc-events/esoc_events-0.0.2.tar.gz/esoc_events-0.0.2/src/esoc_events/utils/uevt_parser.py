from typing import Any

from esoc_events.utils.evtc_parser import EvtcParser


class UevtParser(EvtcParser):

    def __init__(self, path: Any) -> None:
        EvtcParser.__init__(self, path)
