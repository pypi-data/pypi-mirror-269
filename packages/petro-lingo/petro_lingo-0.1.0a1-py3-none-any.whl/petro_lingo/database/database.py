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

import tempfile
import uuid
from pathlib import Path

import numpy as np
import pandas as pd
from geoh5py.data.data_type import DataType
from geoh5py.objects import ObjectBase
from geoh5py.shared.concatenation import Concatenator

from ..shared.utils import ensure_instance, select_data_for_export

COMPUTED_TEXT = object()


class Database:
    """
    The database class to store the data and the results.

    :param source: the data to store in the database.
    """

    def __init__(self, source: ObjectBase | Concatenator):
        # store the data
        self._source: ObjectBase | Concatenator = ensure_instance(
            "source", source, (ObjectBase, Concatenator)
        )

        self._database: pd.DataFrame = pd.DataFrame()
        self._columns: pd.DataFrame = pd.DataFrame(
            columns=["name", "association", "value_map"]
        ).set_index("name")
        self._text_data: dict = {}
        self._metadata: dict = {}

    def _link_data_to_object(self, name: str):
        """
        Link the data to the object of the class.

        :param name: The name of the data to link.
        """
        if name not in self._columns.index.tolist():
            raise KeyError(f"The column '{name}' is not in the database.")

        if isinstance(self.source, Concatenator):
            self.source.drillholes_tables[
                self._columns.at[name, "association"]
            ].add_values_to_property_group(
                name,
                self._database[name].values.astype(np.int32),
                data_type=DataType(
                    self.source.workspace,
                    name=name,
                    primitive_type="REFERENCED",
                    value_map=self._columns.at[name, "value_map"],
                ),
            )

        else:
            value_dict = {
                "values": self._database[name].values.flatten().astype(np.int32),
                "association": self._columns.at[name, "association"],
            }

            if self._columns.at[name, "value_map"]:
                value_dict["type"] = "referenced"
                value_dict["value_map"] = self._columns.at[name, "value_map"]

            self.source.add_data({name: value_dict})

    def _link_file_to_object(self, column: str):
        """
        Link the file to the object of the class.

        :param column: The column to link.
        """
        # Create a temporary file with a specific name prefix
        path = str(tempfile.gettempdir()) + "/" + column + ".txt"

        # Convert file descriptor to a file object
        with open(path, "w+", encoding="utf-8") as temp_file:
            # Write data to the temporary file
            temp_file.write(self._text_data[column])

        # add the file to the object
        file = self.source.add_file(path)

        if isinstance(self.source, Concatenator):
            file.association = "Group"

        # remove the file
        Path(path).unlink()

    def add_text(self, name: str, text: str, metadata: dict | None = None):
        """
        Add a text data to the database.

        :param name: The name of the text data.
        :param text: The text to add.
        :param metadata: The metadata of the text data.
        """
        self._text_data[ensure_instance("name", name, str)] = ensure_instance(
            "name", text, str
        )

        if metadata:
            self._metadata[name] = metadata

    def add_data(
        self,
        data: pd.Series,
        association: str,
        metadata: dict | None = None,
        value_map: dict | None = None,
    ):
        """
        Add a data to the database.

        :param data: The data to add.
        :param association: The association of the data.
        :param metadata: The metadata of the data.
        :param value_map: The value map of the data.
        """
        # append the data to the database
        if self._database.empty:
            self._database = pd.DataFrame(data)
        else:
            if len(data) != len(self._database):
                raise ValueError(
                    "The data to add has a different length than the database."
                )
            if data.name in self._database.columns:
                raise ValueError(
                    f"The column '{data.name}' is already in the database."
                )
            self._database[data.name] = data

        # Precise the association of the data
        self._columns.loc[data.name, "association"] = ensure_instance(
            "association", association, str
        )
        self._columns.at[data.name, "value_map"] = ensure_instance(
            "value_map", value_map, (dict, type(None))
        )

        if metadata:
            self._metadata[data.name] = metadata

    @property
    def created_text_data(self) -> list[str]:
        """
        The names of the created text data.
        """
        return list(self._text_data.keys())

    @property
    def created_vector_data(self) -> list[str]:
        """
        The names of the created text data.
        """
        return self._columns.index.tolist()

    def get_association_from_name(self, name: str | uuid.UUID) -> str:
        """
        Get the association from the name of the data.
        If it's a Concatenator, get the property group name;
        it returns the data association name if Object.

        :param name: the name of the data to extract

        :return: the name of the association
        """
        if isinstance(self.source, Concatenator):
            _name: str = ensure_instance("name", name, str)  # type: ignore
            property_tables = self.source.drillholes_table_from_data_name
            # get the name of the property_group
            if _name not in property_tables:
                raise KeyError(f"The data '{_name}' is not in the object data.")

            return property_tables[_name].name

        data_source = self.source.get_data(name)
        data = data_source[0] if len(data_source) > 0 else None
        association = getattr(data, "association", None)
        if association is None:
            raise ValueError(f"The data '{name}' has no 'association' attribute.")
        return association.name

    def get_column(self, column_key: str | uuid.UUID) -> pd.Series:
        """
        Get a column from the database.

        :param column_key: the name of the column to get.

        :return: the column as a Series
        """
        data = pd.Series(dtype=str)

        if isinstance(self.source, Concatenator):
            column_name: str = ensure_instance("column_name", column_key, str)  # type: ignore
            property_tables = self.source.drillholes_table_from_data_name
            # get the name of the property_group
            if column_name not in property_tables:
                raise KeyError(f"The column '{column_name}' is not in the object data.")

            data = pd.Series(
                property_tables[column_name].depth_table_by_name(
                    column_name, spatial_index=False
                )[column_name],
                name=column_name,
                dtype=str,
            )

        if isinstance(self.source, ObjectBase):
            data = self.source.get_data(column_key)
            if len(data) != 1:
                raise KeyError(
                    f"The column '{column_key}' is not in the object data or duplicated."
                )
            data = pd.Series(data[0].values, name=data[0].name, dtype=str)

        return data

    def export_created_text_data(
        self,
        selected_columns: list[str] | str,
    ):
        """
        Export the selected created data to the object.
        The name of the data contains the name of the column and the time of the export.

        :param selected_columns: the names of the columns to export.
        """
        selected_text = select_data_for_export(selected_columns, self.created_text_data)

        for column in selected_text:
            self._link_file_to_object(column)
            self.source.metadata = {f"PetroLingo_{column}": self._metadata[column]}

    def export_created_vector_data(
        self,
        selected_columns: list[str] | str,
    ):
        """
        Export the selected created data to the object.

        :param selected_columns: The names of the columns to export.
        """
        selected_columns = select_data_for_export(
            selected_columns, self._database.columns.tolist()
        )

        for column in selected_columns:
            self._link_data_to_object(column)
            self.source.metadata = {f"PetroLingo_{column}": self._metadata[column]}

    @property
    def source(self) -> ObjectBase | Concatenator:
        """
        The Object of the database.

        Creates a pointer to the active workspace to ensure the instance
        is active.
        """
        source_pointer = self._source.workspace.get_entity(self._source.uid)[0]

        if not isinstance(source_pointer, (ObjectBase, Concatenator)):
            raise TypeError("The source must be an ObjectBase or a Concatenator.")

        return source_pointer
