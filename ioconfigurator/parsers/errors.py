class NotInit(Exception):
    def __init__(self, ws_name: str, columns: list[str]):
        self.ws_name = ws_name
        self.missed_columns = columns


class WrongExtension(Exception):
    def __init__(self, extension: str):
        self.extension = extension
