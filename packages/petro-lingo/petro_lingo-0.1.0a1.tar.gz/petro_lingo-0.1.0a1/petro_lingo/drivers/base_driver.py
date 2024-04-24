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

import logging
from abc import abstractmethod
from pathlib import Path

from geoh5py.data import Data
from geoh5py.objects import ObjectBase
from geoh5py.shared.concatenation.concatenator import Concatenator
from geoh5py.shared.utils import fetch_active_workspace
from geoh5py.ui_json import InputFile, monitored_directory_copy
from geoh5py.workspace import Workspace
from pydantic import BaseModel, ConfigDict

from ..database.database import Database
from ..engine.engine import Engine
from ..model.model_factory import get_model
from ..shared.geoh5py_utils import get_multi_data_from_ui_json
from ..shared.utils import ensure_instance

logging.basicConfig(level=logging.INFO)

SIZE_TOKENS = {
    "small": 150,
    "medium": 300,
    "large": 600,
}

USER = "geologist"


class LocalBaseDriver:
    """
    This class redefined BaseDriver with pydantic parameters.

    :param params: The parameters of the driver.
    """

    def __init__(self, params: Params):
        self._workspace: Workspace | None = None
        self._out_group: str | None = None
        self._params: Params
        self.params = params

        self._logger = logging.getLogger(__name__)

    @property
    def logger(self) -> logging.Logger:
        """
        The logger of the driver.
        """
        return self._logger

    @property
    def params(self) -> Params:
        """Application parameters as pydantic class."""
        return self._params

    @params.setter
    def params(self, params: Params):
        self._params = ensure_instance("params", params, Params)

    def update_monitoring_directory(self, entity: ObjectBase):
        """
        Push the object to the monitoring directory, if it does not exist,
            push it to the workspace.

        :param object_to_push: the geoh5py entity or group to push.
        """
        if not self.params.monitoring_directory:
            self.logger.info(
                "No 'monitoring directory' found; the results were written to %s.",
                entity.workspace.h5file,
            )
        else:
            monitored_directory_copy(self.params.monitoring_directory, entity)
            self.logger.info("Object %s exported successfully!", entity.name)

    @property
    def workspace(self):
        """Application workspace."""
        if self._workspace is None and self._params is not None:
            self._workspace = self._params.geoh5

        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Application workspace."""

        if not isinstance(workspace, Workspace):
            raise TypeError(
                "Input value for `workspace` must be of type geoh5py.Workspace."
            )

        self._workspace = workspace


class Params(BaseModel):
    """
    The base parameters of the driver.

    :param drillholes: The drillholes Concatenator and data name to use.
    :param my_object: The geoh5py object to use.
    :param data: The data linked to the object to use.
    :param model: The name of the LargeLanguage model to use.
    :param monitored_directory: the path to the temporary directory workspace to monitor.
    :param geoh5: The path to the workspace file containing the object to modify.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    drillholes: dict | None
    my_object: ObjectBase | None
    data: Data | None
    model: str
    monitoring_directory: str | None
    geoh5: Workspace
    user: str = USER


class EngineDriver(LocalBaseDriver):
    """
    The driver of the engine ; prepares the class to be used and run the different operations.

    :param params: The parameters of the ui.json file.
    """

    _engine_type: type[Engine] = Engine
    _params_type: type[Params] = Params
    _application: str = "abstract"
    _input_keys: dict[str, list[str]] = {"drillholes": ["groupValue", "value"]}

    def __init__(
        self,
        params: Params,
    ):
        super().__init__(params)  # type: ignore

        self._language_model = get_model(
            self.params.model, self._application, self.params.user
        )
        self._created: dict = {"text": [], "data": []}

        self._data: str | Data
        self._object: ObjectBase | Concatenator

        self._prepare_params()
        self._engine: Engine = self._engine_type(
            Database(self._object), self._language_model
        )

    def _additional_params_preparation(self):
        """
        Prepare the additional parameters of the model.

        It's not doing anything by default.
        For given model, it should be overwritten to get some specifics arguments.
        """

    def _prepare_params(self):
        """
        Prepare the parameters of the model.

        As the parameters are coming from the ui.json file,
        No type verification are conducted.
        """
        if self._params.drillholes["groupValue"] is not None:  # type: ignore
            self._object = self._params.drillholes["groupValue"]  # type: ignore
            self._data = self._params.drillholes["value"][0]  # type: ignore
        else:
            self._object = self._params.my_object  # type: ignore
            self._data = self._params.data.uid  # type: ignore

        self._additional_params_preparation()

    def export_created_data(self):
        """
        Export the created data of the engine.

        Once exported, the created data are reset.
        """
        if self._created["text"]:
            self._engine.database.export_created_text_data(self._created["text"])
        if self._created["data"]:
            self._engine.database.export_created_vector_data(self._created["data"])

        # reset created
        self._created = {"text": [], "data": []}

    @abstractmethod
    def run_engine(self):
        """
        Run the engine with the given parameters.
        """

    def run(self):
        """
        Run the inference of the model. The model is modified and pushed back to the workspace.
        """
        with fetch_active_workspace(self.workspace, mode="r+"):
            self.logger.info("Process started, please wait...")
            self.run_engine()
            self.export_created_data()
            self.update_monitoring_directory(self._engine.database.source)  # type: ignore

    @property
    def size(self) -> dict:
        """
        Return the size of the tokens for the summary.
        """  # todo: should it depend of the model?
        return SIZE_TOKENS

    @classmethod
    def start(cls, path: str | Path) -> EngineDriver:
        """
        Start a driver with a given ui.json path.

        :param path: The path to the ui.json file.

        :return: A new instance of the driver.
        """
        input_file = InputFile.read_ui_json(path)
        data = get_multi_data_from_ui_json(input_file, cls._input_keys)
        return cls(cls._params_type(**data))
