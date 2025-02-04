from typing import NamedTuple


class ParsedLine(NamedTuple):
    nLine: int
    nSignal: str
    nSignalRef: int
    symbol: str
    name: str
    typeRawSignal: str
    min: str
    max: str
    units: str
    plc: str
    nModule: str
    typeModule: str
    nChannel: str
    typeChannel: str
    # typeContact: str
    typeSignal: str
    box: str
    errors: list[int] | None
