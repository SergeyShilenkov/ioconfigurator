from pathlib import Path

from processor.processor import ProcessedData


def _header(title: str) -> str:
    return f'{100*"="}\n{100*"="}\n{title}\n{100*"="}\n{100*"="}\n\n'


def _generate_structs(data: list[ProcessedData]) -> str:
    _strDgo = ['TYPE strDgo :\nSTRUCT']
    _strDgoClass = ['TYPE strDgoClass :\nSTRUCT']
    _strDgo_cmd = ['TYPE strDgo_cmd :\nSTRUCT']

    for s in data:
        _strDgo.append(f'\t{s.tag} : BOOL; // {s.descr}')
        _strDgoClass.append(f'\t{s.tag} : signals.fbDgo; // {s.descr}')
        _strDgo_cmd.append(f'\t{s.tag} : signals.strDgoCmd; // {s.descr}')

    _strDgo.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strDgoClass.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strDgo_cmd.append('END_STRUCT\nEND_TYPE')

    return '\n'.join(_strDgo + _strDgoClass + _strDgo_cmd)


def _generate_meth_init(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'_settings.inverse := {s.inverse}; // Инверсия параметра')

        _text.append(f'gvl.dgoClass.{s.tag}.methInit(settings := _settings);\n\n')

    return '\n'.join(_text)


def _generate_meth_proc(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgoClass.{s.tag}.methProc(raw := gvl.dgo.{s.tag}, cmd := gvl.dgoCmd.{s.tag});')

    return '\n'.join(_text)


def _generate_meth_reference(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.dgoClass.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.dgoReference[{s.n_ref}].block REF= gvl.dgoClass.{s.tag};\n')

    return '\n'.join(_text)


def _generate_meth_upload(data: list[ProcessedData]) -> str:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.dgoClass.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, swap_bytes := FALSE); // {s.descr}')

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
