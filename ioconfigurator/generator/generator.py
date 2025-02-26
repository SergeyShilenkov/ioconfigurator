import os
import shutil
import sys
from pathlib import Path
from typing import Any

from ioconfigurator.generator.generators import ai, ao, di, do


__all__ = ['generate_code']


_GENERATORS = {
    'ai': ai.generate,
    'ao': ao.generate,
    'di': di.generate,
    'do': do.generate,
}


def _generate(path: Path, channel_type: str, data: list[Any]):
    dir_path = Path(path, channel_type)
    os.mkdir(dir_path)

    try:
        _GENERATORS[channel_type.lower()](dir_path, data)
    except KeyError:
        print(f'Нет генератора для {channel_type} сигналов')
        sys.exit(1)


def generate_code(path: Path, data: dict[str, list[Any]]):
    # Очищаем/создаём папку со сгенерированным кодом
    code_dir_path = Path(path.parent, '_code/')
    if code_dir_path.exists():
        shutil.rmtree(code_dir_path)
    os.mkdir(code_dir_path)

    # Генерируем код
    for channel_type in data:
        _generate(code_dir_path, channel_type, data[channel_type])


if __name__ == '__main__':
    pass
