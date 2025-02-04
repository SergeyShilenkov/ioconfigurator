from pathlib import Path

from processor.processor import ProcessedData


def _header(title: str) -> str:
    return f'{100*"="}\n{100*"="}\n{title}\n{100*"="}\n{100*"="}\n\n'


def _generate_structs(data: list[ProcessedData]) -> str:
    _strDgiClass = ['TYPE strDgiClass :\nSTRUCT']
    _strDgi_cmd = ['TYPE strDgi_cmd :\nSTRUCT']
    _strDgi_drv = ['TYPE strDgi_drv :\nSTRUCT']

    for s in data:
        _strDgiClass.append(f'\t{s.tag} : signals.fbDgi; // {s.descr}')
        _strDgi_cmd.append(f'\t{s.tag} : signals.fbDgiCmd; // {s.descr}')
        _strDgi_drv.append(f'\t{s.tag} : BOOL; // {s.descr}')

    _strDgiClass.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strDgi_cmd.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strDgi_drv.append('END_STRUCT\nEND_TYPE')

    return '\n'.join(_strDgiClass + _strDgi_cmd + _strDgi_drv)


def _generate_meth_init(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append('_settings.repair_time := 10.0; // Ремонт. Время нахождения канала в ремонте')
        _text.append('_settings.dnd := 0.0; // Задержка дребезга, с')
        _text.append(f'_settings.inverse := {s.inverse}; // Инверсия параметра')

        _text.append(f'gvl.dgi.{s.tag}.methInit(settings := _settings);\n\n')

    return '\n'.join(_text)


def _generate_meth_proc(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgi.{s.tag}.methProc(raw := gvl.dgiDrv.{s.tag}, cmd := gvl.dgiCmd.{s.tag});')

    return '\n'.join(_text)


def _generate_meth_reference(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgi.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.dgiReference[{s.n_ref}].block REF= gvl.dgi.{s.tag};\n')

    return '\n'.join(_text)


def _generate_meth_upload(data: list[ProcessedData]) -> str:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.dgi.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, swap_bytes := FALSE); // {s.descr}')

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
