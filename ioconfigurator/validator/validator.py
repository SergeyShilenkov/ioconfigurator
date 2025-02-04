import logging
from pathlib import Path
from typing import Callable

from parsers.parser import model
# from validator.checks import ai, ao, di, do, general
from validator.checks import ai, general


__all__ = ['Validator']


ERRORS = {
    0: '',
    1: '',
}


class Validator:
    def __init__(self, path: Path, data: list[model.ParsedLine], variables: dict[str, str] | None, exceptions: bool):
        if not exceptions:
            self._logger = self._get_logger(path)
            self._logger.info('Поехали!')

        self._signals = data
        self._vars = variables
        self._checks = {
            'general': general.checks(),
            'ai': ai.checks(),
            # 'ao': ao.checks(),
            # 'di': di.checks(),
            # 'do': do.checks(),
        }
        self._racks = {}

    @staticmethod
    def _get_logger(path: Path) -> logging.Logger:
        logger = logging.getLogger(__name__)

        logger.setLevel(logging.INFO)

        log_dir_path = Path(path.parent, '_log')
        log_dir_path.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(f"{log_dir_path}/1.log", mode='w')
        handler.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))

        logger.addHandler(handler)

        return logger

    def validate(self):
        if self._signals is None or self._signals == []:
            raise TypeError

        # for signal in self._signals:
        #     for check in self._checks['general']:
        #         check(signal)
        #     for check in self._checks[signal.typeChannel.lower()]:
        #         check(signal)


if __name__ == '__main__':
    pass
