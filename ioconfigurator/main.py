"""
IO-конфигуратор для систем управления двигателями (СУД) производства «Альянс Эко»
run: python .\ioconfigurator\main.py -p "path\to\io list.xlsx" -pv "path\to\vars.xlsx" -e "A1 ШУ" "A2 ШУД" "A3 ШУ" -ai -ao -di -do -ex
"""
import argparse
import sys
from pathlib import Path
from typing import Type

from generator.generator import generate_code
from parsers.parser import ParserIO, ParserVars, model
from processor.processor import data_processing
from validator.validator import Validator
from parsers import errors


def _parse_args() -> argparse.Namespace:
    """
    парсинг параметров командной строки
    """
    parser_args = argparse.ArgumentParser(description='Generate code for CoDeSys. IF -ai and -ao and -di and -do are '
                                                      'not specified then everything is generated')
    parser_args.add_argument('-p', metavar='Path', type=Path, help='path to io-file.xlsx', required=True)
    parser_args.add_argument('-pv', metavar='PathVars', type=Path, help='path to vars.xlsx')
    parser_args.add_argument('-e', nargs='+', help='exclude specific PLCs')
    parser_args.add_argument('-ai', help='Generate AI-data', action="store_true")
    parser_args.add_argument('-ao', help='Generate AO-data', action="store_true")
    parser_args.add_argument('-di', help='Generate DI-data', action="store_true")
    parser_args.add_argument('-do', help='Generate DO-data', action="store_true")
    parser_args.add_argument('-ex', help='exceptions over log', action="store_true")

    args = parser_args.parse_args()

    if not args.ai and not args.ao and not args.di and not args.do:
        args.ai, args.ao, args.di, args.do = True, True, True, True

    return args


def _parse_xlsx(path: Path, parser: Type[ParserIO] | Type[ParserVars], **kwargs) -> list[model.ParsedLine] | dict[str, str]:
    """
    парсинг эксель файлов
    """
    try:
        data = parser(path).parse(**kwargs)
    except FileExistsError:
        print(f'ОШИБКА!\nФайла: {path} не существует.')
        sys.exit(1)
    except errors.WrongExtension as e:
        print(f'ОШИБКА!\nФайл: {path}\nНеподдерживаемое расширение файла: {e.extension}')
        sys.exit(1)
    except errors.NotInit as e:
        print(f'ОШИБКА!\nФайл: {path}\nЛист: {e.ws_name}\nНедостающие столбцы: {", ".join(e.missed_columns)}')
        sys.exit(1)

    return data


def main():
    # command line arguments
    args = _parse_args()

    # Парсинг данных из io.xlsx
    data = _parse_xlsx(path=args.p, parser=ParserIO, exclude=args.e, ai=args.ai, ao=args.ao, di=args.di, do=args.do)

    # Парсинг наименования переменных из vars.xlsx, если файл указан
    variables = None
    if args.pv is not None:
        variables = _parse_xlsx(path=args.pv, parser=ParserVars)

    # Валидация данных
    Validator(path=args.p, data=data, variables=variables, exceptions=args.ex).validate()

    # Подготовка данных
    processed_data = data_processing(data=data, variables=variables)

    # Создание файлов с кодом
    generate_code(path=args.p, data=processed_data)


if __name__ == '__main__':
    main()
