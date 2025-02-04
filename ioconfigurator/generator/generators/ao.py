from pathlib import Path

from processor.processor import ProcessedData


def _header(title: str) -> str:
    return f'{100*"="}\n{100*"="}\n{title}\n{100*"="}\n{100*"="}\n\n'


def _generate_structs(data: list[ProcessedData]) -> str:
    _strAoClass = ['TYPE strAoClass :\nSTRUCT']
    _strAo_ = ['TYPE strAo_ :\nSTRUCT']
    _strAo_cmd = ['TYPE strAo_cmd :\nSTRUCT']

    for s in data:
        _strAoClass.append(f'\t{s.tag} : signals.fbAo; // {s.descr}')
        _strAo_.append(f'\t{s.tag} : REAL; // {s.descr}')
        _strAo_cmd.append(f'\t{s.tag} : signals.strAoCmd; // {s.descr}')

    _strAoClass.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strAo_.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strAo_cmd.append('END_STRUCT\nEND_TYPE')

    return '\n'.join(_strAoClass + _strAo_ + _strAo_cmd)


def _generate_meth_init(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'_settings.adc_min := {s.min_adc}; // АЦП. Минимальное значение')
        _text.append(f'_settings.adc_max := {s.max_adc}; // АЦП. Максимальное значение')

        _text.append(f'_settings.scale_max := {s.scale_max}; // Верхнее значение шкалы датчика')
        _text.append(f'_settings.scale_min := {s.scale_min}; // Нижнее значение шкалы датчика')

        _text.append(f'gvl.aoClass.{s.tag}.methInit(settings := _settings);\n\n')

    return '\n'.join(_text)


def _generate_meth_proc(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.aoClass.{s.tag}.methProc(raw := gvl.ao.{s.tag}, cmd := gvl.aoCmd.{s.tag});')

    return '\n'.join(_text)


def _generate_meth_reference(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.aoClass.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.aoReference[{s.n_ref}].block REF= gvl.aoClass.{s.tag};\n')

    return '\n'.join(_text)


def _generate_meth_upload(data: list[ProcessedData]) -> str:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.aoClass.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, swap_bytes := FALSE); // {s.descr}')

    return '\n'.join(_text)


def generate(path: Path, data: list[ProcessedData]) -> None:
    with open(path, 'w') as f:
        f.write(_header('СТРУКТУРЫ'))
        f.write(_generate_structs(data))
        f.write('\n\n')

        f.write(_header('methInit'))
        f.write(_generate_meth_init(data))
        f.write('\n\n')

        f.write(_header('methProc'))
        f.write(_generate_meth_proc(data))
        f.write('\n\n')

        f.write(_header('methReference'))
        f.write(_generate_meth_reference(data))
        f.write('\n\n')

        f.write(_header('methUpload'))
        f.write(_generate_meth_upload(data))


if __name__ == '__main__':
    pass
