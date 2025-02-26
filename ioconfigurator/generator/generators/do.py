from pathlib import Path

from ioconfigurator.processor.processor import ProcessedData


def _generate_str_dgo(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strDgo :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : BOOL; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strDgo.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_dgo_class(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strDgoClass :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.fbDgo; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strDgo.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_dgo_cmd(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strDgo_cmd :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.strDgoCmd; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strDgo.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_init(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'_settings.inverse := {s.inverse}; // Инверсия параметра')

        _text.append(f'gvl.dgoClass.{s.tag}.methInit(settings := _settings);\n\n')

    with open(Path(path, 'methInit.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_proc(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgoClass.{s.tag}.methProc(raw := gvl.dgo.{s.tag}, cmd := gvl.dgoCmd.{s.tag});')

    with open(Path(path, 'methProc.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_reference(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgoClass.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.dgoReference[{s.n_ref}].block REF= gvl.dgoClass.{s.tag};\n')

    with open(Path(path, 'methReference.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_upload(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.dgoClass.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, '
                     f'swap_bytes := FALSE); // {s.descr}')

    with open(Path(path, 'methUpload.txt'), 'w') as f:
        f.write('\n'.join(_text))


def generate(path: Path, data: list[ProcessedData]) -> None:
    _generate_str_dgo(path, data)

    _generate_str_dgo_class(path, data)

    _generate_str_dgo_cmd(path, data)

    _generate_meth_init(path, data)

    _generate_meth_proc(path, data)

    _generate_meth_reference(path, data)

    _generate_meth_upload(path, data)


if __name__ == '__main__':
    pass
