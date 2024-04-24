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

# pylint: disable=too-few-public-methods
from __future__ import annotations

import sys

from petro_lingo.drivers.base_driver import EngineDriver, Params
from petro_lingo.engine.engine import ReloggerEngine


class ReloggerParams(Params):
    """
    The parameters for the ask driver.

    :param classes: The classes to relog as one string separated by ', '.
    """

    classes: str


class ReloggerDriver(EngineDriver):
    """
    The driver class to run the relogger model.
    """

    _engine_type = ReloggerEngine
    _params_type = ReloggerParams
    _application = "relog"

    def __init__(self, params: ReloggerParams):
        super().__init__(params)

        self._classes: list[str]

    def _additional_params_preparation(self):
        self._classes = self.params.classes.split(", ")

    def run_engine(self):
        self._engine.model.classes = self._classes

        name = self._engine.relog(column=self._data)  # type: ignore

        self._created["data"].append(name)


if __name__ == "__main__":  # pragma: no
    file = sys.argv[1]
    ReloggerDriver.start(file).run()
