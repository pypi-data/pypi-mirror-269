# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024 Mira Geoscience Ltd.                                     '
#  All rights reserved.                                                        '
#                                                                              '
#  This file is part of Petro-Lingo.                                           '
#                                                                              '
#  The software and information contained herein are proprietary to, and       '
#  comprise valuable trade secrets of, Mira Geoscience, which                  '
#  intend to preserve as trade secrets such software and information.          '
#  This software is furnished pursuant to a written license agreement and      '
#  may be used, copied, transmitted, and stored only in accordance with        '
#  the terms of such license and with the inclusion of the above copyright     '
#  notice.  This software and information or any other copies thereof may      '
#  not be provided or otherwise made available to any other person.            '
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from __future__ import annotations

from typing import TypeVar

TYPE = TypeVar("TYPE")  # pylint: disable=invalid-name


def ensure_instance(name: str, value: TYPE, type_: type | tuple) -> TYPE:
    """
    Ensure the value is an instance of the type.

    :param name: The name of the value.
    :param value: The value to check.
    :param type_: The type to check.

    :return: The value as the type.
    """
    if not isinstance(value, type_):
        raise TypeError(
            f"The attribute '{name}' must be an instance of '{type_}'."
            f"Value of type '{type(value)}' provided."
        )

    return value


def prepare_metadata(function: str, name: str, **parameters) -> dict:
    """
    Prepare the metadata of an outptut.

    :param function: The function used to compute the output.
    :param name: The name of the input.
    :param parameters: The parameters used to compute the output.

    :return: The metadata of the output.
    """

    metadata = {
        "name": name,
        "function": function,
    }

    if parameters:
        metadata.update(parameters)

    return metadata


def select_data_for_export(
    selected_columns: list[str] | str,
    existing_data: list[str],
) -> list[str]:
    """
    Select the data to export.

    :param selected_columns: the names of the columns to export.
    :param existing_data: the names of the existing data.

    :return: The actual names of the columns to export.
    """
    # only select selected_columns in selected data
    if isinstance(selected_columns, str):
        selected_columns = [selected_columns]

    selected_data = list(
        set(ensure_instance("existing_data", existing_data, list)).intersection(
            ensure_instance("selected_columns", selected_columns, list)
        )
    )

    if len(selected_data) == 0:
        raise KeyError(f"No name found: '{selected_columns}' in '{existing_data}'.")

    return selected_data
