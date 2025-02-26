from pathlib import Path

from ioconfigurator.processor.processor import ProcessedData


def _generate_str_dgi_class(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strDgiClass :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.fbDgi; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strDgiClass.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_dgi_cmd(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strDgi_cmd :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.fbDgiCmd; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strDgiClass.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_dgi_drv(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strDgi_drv :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : BOOL; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strDgiClass.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_init(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append('_settings.repair_time := 10.0; // Ремонт. Время нахождения канала в ремонте\n'
                     '_settings.dnd := 0.0; // Задержка дребезга, с')
        _text.append(f'_settings.inverse := {s.inverse}; // Инверсия параметра')

        _text.append(f'gvl.dgi.{s.tag}.methInit(settings := _settings);\n\n')

    with open(Path(path, 'methInit.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_proc(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgi.{s.tag}.methProc(raw := gvl.dgiDrv.{s.tag}, cmd := gvl.dgiCmd.{s.tag});')

    with open(Path(path, 'methProc.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_reference(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgi.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.dgiReference[{s.n_ref}].block REF= gvl.dgi.{s.tag};\n')

    with open(Path(path, 'methReference.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_upload(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.dgi.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, swap_bytes := FALSE); // {s.descr}')

    with open(Path(path, 'methUpload.txt'), 'w') as f:
        f.write('\n'.join(_text))


def generate(path: Path, data: list[ProcessedData]) -> None:
    _generate_str_dgi_class(path, data)

    _generate_str_dgi_cmd(path, data)

    _generate_str_dgi_drv(path, data)

    _generate_meth_init(path, data)

    _generate_meth_proc(path, data)

    _generate_meth_reference(path, data)

    _generate_meth_upload(path, data)


if __name__ == '__main__':
    pass
