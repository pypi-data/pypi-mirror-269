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

# pylint: disable=too-few-public-methods, duplicate-code
from __future__ import annotations

import sys

from petro_lingo.drivers.base_driver import EngineDriver, Params
from petro_lingo.engine.engine import SynthesizerEngine


class SummaryParams(Params):
    """
    The parameters for the ask driver.

    :param size: The size of the answer as a string.
    """

    size: str


class SummaryDriver(EngineDriver):
    """
    The driver class to run the synthesizer model.
    """

    _engine_type = SynthesizerEngine
    _params_type = SummaryParams
    _application = "synthesize"

    def run_engine(self):
        name = self._engine.summarize(  # type: ignore
            column=self._data, tokens_resize=self.size[self.params.size]
        )

        self._created["text"].append(name)


if __name__ == "__main__":  # pragma: no cover
    file = sys.argv[1]
    SummaryDriver.start(file).run()
