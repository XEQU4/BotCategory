import json
from pathlib import Path


async def get_client_text(file_name: str, func: str, index: int = None) -> str:
    """
    Get clients texts

    :param file_name: file name
    :param func: function name
    :param index: text index in list
    :return: text
    """
    path = Path("handlers") / "client_handlers" / "texts" / "texts.json"
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    if index is None:
        return data[file_name][func]

    else:
        return data[file_name][func][index]