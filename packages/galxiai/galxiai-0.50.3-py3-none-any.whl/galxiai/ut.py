import json
import os
from typing import Tuple, Union

from galxiai.const import Galxi


def _save_bytes_c(content, file_name):
    """
    save the bytes info into the file
    :param content:
    :param file_name:
    :return:
    """
    file_object = None
    try:
        file_object = open(file_name, 'wb')
        file_object.truncate(0)
    except FileNotFoundError:
        file_object = open(file_name, 'a+')
    finally:
        # file_object.buffer.write(content)
        file_object.write(content)
        file_object.close()


def json_save(content, tmp_file: str = ""):
    if tmp_file is None or tmp_file == "":
        tmp_file = Galxi.TEMP_JSON

    my_str_as_bytes = None

    if isinstance(content, dict):
        my_str_as_bytes = str.encode(json.dumps(content))

    if isinstance(content, str):
        my_str_as_bytes = str.encode(content)

    if my_str_as_bytes is None:
        my_str_as_bytes = content

    path = os.path.join(Galxi.CACHE_PATH, tmp_file)
    _save_bytes_c(my_str_as_bytes, path)


def obj_to_string(update_config) -> str:
    update_string = ''
    index = 0
    for key, value in update_config.items():
        update_string = update_string + f"{key}='{value}'," if index < len(
            update_config) - 1 else update_string + f"{key}='{value}'"
        index = index + 1

    return update_string


def obj_to_tuple(obj) -> Tuple[str, str]:
    """ Parse JSON object and format it for insert_data method

    Parameters:
        obj (dict): The JSON object that should be formatted

    Returns:
        dict: JSON object with keys and values formatted for insert_data method """

    keys = ''
    values = ''
    for key, value in obj.items():
        keys = f'{keys},{key}' if keys != '' else key
        values = f'{values}, :{key}' if values != '' else f':{key}'

    return keys, values
