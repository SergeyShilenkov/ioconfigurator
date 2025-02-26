from pathlib import Path

from ioconfigurator.processor.processor import ProcessedData


def _generate_str_ao_class(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strAoClass :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.fbAo; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strAoClass.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_ao_(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strAo_ :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : REAL; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strAo_.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_ao_cmd(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strAo_cmd :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.strAoCmd; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strAoCmd.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_init(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'_settings.adc_min := {s.min_adc}; // АЦП. Минимальное значение')
        _text.append(f'_settings.adc_max := {s.max_adc}; // АЦП. Максимальное значение')

        _text.append(f'_settings.scale_max := {s.scale_max}; // Верхнее значение шкалы датчика')
        _text.append(f'_settings.scale_min := {s.scale_min}; // Нижнее значение шкалы датчика')

        _text.append(f'gvl.aoClass.{s.tag}.methInit(settings := _settings);\n\n')

    with open(Path(path, 'methInit.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_proc(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.aoClass.{s.tag}.methProc(raw := gvl.ao.{s.tag}, cmd := gvl.aoCmd.{s.tag});')

    with open(Path(path, 'methProc.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_reference(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.aoClass.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.aoReference[{s.n_ref}].block REF= gvl.aoClass.{s.tag};\n')

    with open(Path(path, 'methReference.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_upload(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.aoClass.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, '
                     f'swap_bytes := FALSE); // {s.descr}')

    with open(Path(path, 'methUpload.txt'), 'w') as f:
        f.write('\n'.join(_text))


def generate(path: Path, data: list[ProcessedData]) -> None:
    _generate_str_ao_class(path, data)

    _generate_str_ao_(path, data)

    _generate_str_ao_cmd(path, data)

    _generate_meth_init(path, data)

    _generate_meth_proc(path, data)

    _generate_meth_reference(path, data)

    _generate_meth_upload(path, data)


if __name__ == '__main__':
    pass
