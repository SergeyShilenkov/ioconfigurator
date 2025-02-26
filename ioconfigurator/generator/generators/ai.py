from pathlib import Path

from ioconfigurator.processor.processor import ProcessedData


def _generate_str_ai_class(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strAiClass :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.fbAi; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strAiClass.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_ai_cmd(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strAiCmd :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : signals.strAiCmd; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strAiCmd.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_str_ai_drv(path: Path, data: list[ProcessedData]) -> None:
    _text = ['TYPE strAiDrv :\nSTRUCT']

    for s in data:
        _text.append(f'\t{s.tag} : REAL; // {s.descr}')

    _text.append('END_STRUCT\nEND_TYPE')

    with open(Path(path, 'strAiDrv.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_init(path: Path, data: list[ProcessedData]) -> None:
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

        _text.append('_settings.roc := 0.0; // Допустимая скорость роста\n'
                     '_settings.recovery_time := 5.0; // Время восстановления канала после неисправности, сек.\n'
                     '_settings.repair_time := 3600.0; // Ремонт. Время нахождения канала в ремонте\n'
                     '_settings.tau := 0.0; // Тау фильтра, сек.')

        _text.append(f'gvl.ai.{s.tag}.methInit(settings := _settings);\n\n')

    with open(Path(path, 'methInit.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_proc(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.ai.{s.tag}.methProc(raw := gvl.aiDrv.{s.tag}, cmd := gvl.aiCmd.{s.tag}, check_break_limit '
                     f':= FALSE);')

    with open(Path(path, 'methProc.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_reference(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for s in data:
        _text.append(f'// {s.descr}')
        _text.append(f'gvl.ai.{s.tag}.propSetId := {s.n_ref};')
        _text.append(f'gvl.aiReference[{s.n_ref}].block REF= gvl.ai.{s.tag};\n')

    with open(Path(path, 'methReference.txt'), 'w') as f:
        f.write('\n'.join(_text))


def _generate_meth_upload(path: Path, data: list[ProcessedData]) -> None:
    _text = []

    for idx, s in enumerate(data):
        _cell = 'cell_start' if idx == 0 else 'methUpload'

        _text.append(f'methUpload := gvl.ai.{s.tag}.methUpload(mas := gvl.global_mass, cell := {_cell}, swap_bytes := '
                     f'FALSE); // {s.descr}')

    with open(Path(path, 'methUpload.txt'), 'w') as f:
        f.write('\n'.join(_text))


def generate(path: Path, data: list[ProcessedData]) -> None:
    _generate_str_ai_class(path, data)

    _generate_str_ai_cmd(path, data)

    _generate_str_ai_drv(path, data)

    _generate_meth_init(path, data)

    _generate_meth_proc(path, data)

    _generate_meth_reference(path, data)

    _generate_meth_upload(path, data)


if __name__ == '__main__':
    pass
