from pathlib import Path

from processor.processor import ProcessedData


def _header(title: str) -> str:
    return f'{100*"="}\n{100*"="}\n{title}\n{100*"="}\n{100*"="}\n\n'


def _generate_structs(data: list[ProcessedData]) -> str:
    _strAiClass = ['TYPE strAiClass :\nSTRUCT']
    _strAi_cmd = ['TYPE strAiClass :\nSTRUCT']
    _strAi_drv = ['TYPE strAiClass :\nSTRUCT']

    for s in data:
        _strAiClass.append(f'\t{s.tag} : signals.fbAi; // {s.descr}')
        _strAi_cmd.append(f'\t{s.tag} : signals.strAiCmd; // {s.descr}')
        _strAi_drv.append(f'\t{s.tag} : REAL; // {s.descr}')

    _strAiClass.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strAi_cmd.append('END_STRUCT\nEND_TYPE\n\n\n')
    _strAi_drv.append('END_STRUCT\nEND_TYPE')

    return '\n'.join(_strAiClass + _strAi_cmd + _strAi_drv)


def _generate_meth_init(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'_settings.adc_min := {s.min_adc}; // АЦП. Минимальное значение')
        _text.append(f'_settings.adc_max := {s.max_adc}; // АЦП. Максимальное значение')

        _text.append(f'_settings.scale_max := {s.scale_max}; // Верхнее значение шкалы датчика')
        _text.append(f'_settings.scale_min := {s.scale_min}; // Нижнее значение шкалы датчика')

        _text.append(f'_settings.limit_hi := {s.limit_hi}; // Зашкал вверх')
        _text.append(f'_settings.limit_lo := {s.limit_lo}; // Зашкал низ')
        _text.append(f'_settings.break_hi := {s.break_hi}; // Обрыв вверх')
        _text.append(f'_settings.break_lo := {s.break_lo}; // Обрыв низ')

        _text.append('_settings.roc := 0.0; // Допустимая скорость роста')
        _text.append('_settings.recovery_time := 5.0; // Время восстановления канала после неисправности, сек.')
        _text.append('_settings.repair_time := 3600.0; // Ремонт. Время нахождения канала в ремонте')
        _text.append('_settings.tau := 0.0; // Тау фильтра, сек.')

        _text.append(f'gvl.ai.{s.tag}.methInit(settings := _settings);\n\n')

    return '\n'.join(_text)


def _generate_meth_proc(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.ai.{s.tag}.methProc(raw := gvl.aiDrv.{s.tag}, cmd := gvl.aiCmd.{s.tag}, check_break_limit := FALSE);')

    return '\n'.join(_text)


def _generate_meth_reference(data: list[ProcessedData]) -> str:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.ai.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.aiReference[{s.n_ref}].block REF= gvl.ai.{s.tag};\n')

    return '\n'.join(_text)


def _generate_meth_upload(data: list[ProcessedData]) -> str:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.ai.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, swap_bytes := FALSE); // {s.descr}')

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
