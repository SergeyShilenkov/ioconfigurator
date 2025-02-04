import os
import shutil
import sys
from pathlib import Path
from typing import Any

from generator.generators import ai, ao, di, do


__all__ = ['generate_code']


def generate_code(path: Path, data: dict[str, list[Any]]):
    _generators = {
        'ai': ai.generate,
        'ao': ao.generate,
        'di': di.generate,
        'do': do.generate,
    }

    # Очищаем/создаём папку со сгенерированным кодом
    code_dir_path = Path(path.parent, '_code/')
    if code_dir_path.exists():
        shutil.rmtree(code_dir_path)
    os.mkdir(code_dir_path)

    # Генерируем код
    for channel_types in data:
        try:
            _generators[channel_types.lower()](Path(path.parent, f'_code/{channel_types}.txt'), data[channel_types])
        except KeyError:
            print(f'Нет генератора для {channel_types} сигналов')
            sys.exit(1)


if __name__ == '__main__':
    pass
