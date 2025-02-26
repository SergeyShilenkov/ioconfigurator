from typing import NamedTuple

from ioconfigurator.parsers.parser import model


__all__ = ['ProcessedData', 'data_processing']


class ProcessedData(NamedTuple):
    n_module: int
    n_channel: int
    n_ref: int
    type: str
    tag: str
    descr: str
    inverse: bool
    min_adc: float
    max_adc: float
    scale_min: float | str
    scale_max: float | str
    limit_hi: float
    limit_lo: float
    break_hi: float
    break_lo: float
    units: str
    errors: list[int] | None


def _get_minmax_adc(s: model.ParsedLine, r: bool) -> (float, float):
    if s.typeChannel.lower() != 'ai' and s.typeChannel.lower() != 'ao':
        return 0.0, 0.0

    if r or s.typeSignal.lower() == 'ai_i':
        return 4.0, 20.0

    try:
        _min_adc = float(s.min)
    except ValueError:
        _min_adc = 0.0

    try:
        _max_adc = float(s.max)
    except ValueError:
        _max_adc = 0.0

    return _min_adc, _max_adc


def _get_minmax(s: model.ParsedLine, r: bool) -> (float, float):
    if s.typeChannel.lower() != 'ai' and s.typeChannel.lower() != 'ao':
        return 0.0, 0.0

    if r:
        return 4.0, 20.0

    try:
        _min = float(s.min)
    except ValueError:
        _min = 0.0

    try:
        _max = float(s.max)
    except ValueError:
        _max = 0.0

    return _min, _max


def _get_limits(s: model.ParsedLine) -> (float, float, float, float):
    if s.typeChannel.lower() != 'ai':
        return 0.0, 0.0, 0.0, 0.0

    try:
        _range = float(s.max) - float(s.min)

        _limit_hi = float(s.max) + _range*0.01
        _limit_lo = float(s.min) - _range*0.012
        _break_hi = float(s.max) + _range*0.03
        _break_lo = float(s.min) - _range*0.024
    except ValueError:
        _limit_hi = 0.0
        _limit_lo = 0.0
        _break_hi = 0.0
        _break_lo = 0.0

    return _limit_hi, _limit_lo, _break_hi, _break_lo


def _get_inverse(s: model.ParsedLine) -> bool:
    # return (s.typeChannel.lower() == 'di' or s.typeChannel.lower() == 'do') and s.typeContact.lower() == 'нз'
    return False


def data_processing(data: list[model.ParsedLine], variables: dict[str, str]) -> dict[str, list[ProcessedData]]:
    processed_data: dict[str, list[ProcessedData]] = {}

    for signal in data:
        if signal.typeChannel not in processed_data:
            processed_data[signal.typeChannel] = []

        _reserve = 'резерв' in signal.name.lower()

        _min_adc, _max_adc = _get_minmax_adc(signal, _reserve)
        _min, _max = _get_minmax(signal, _reserve)
        _limit_hi, _limit_lo, _break_hi, _break_lo = _get_limits(signal)
        _inverse = _get_inverse(signal)

        _tag = signal.symbol
        if variables:
            if variables[signal.symbol]:
                _tag = f"{signal.symbol}_{variables[signal.symbol]}"

        processed_data[signal.typeChannel].append(
            ProcessedData(
                n_module=int(signal.nModule),
                n_channel=int(signal.nChannel),
                n_ref=signal.nSignalRef,
                type=signal.typeChannel.lower(),
                tag=_tag,
                descr=signal.name,
                inverse=_inverse,
                min_adc=_min_adc,
                max_adc=_max_adc,
                scale_min=_min,
                scale_max=_max,
                limit_hi=_limit_hi,
                limit_lo=_limit_lo,
                break_hi=_break_hi,
                break_lo=_break_lo,
                units=signal.units,
                errors=signal.errors
            )
        )

    return processed_data


if __name__ == '__main__':
    pass
