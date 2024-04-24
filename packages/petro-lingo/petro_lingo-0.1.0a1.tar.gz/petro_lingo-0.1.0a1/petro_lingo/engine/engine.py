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

import pandas as pd

from ..database.database import Database
from ..model.base_model import LanguageModel
from ..model.inquirer import Inquirer
from ..model.relogger import Relogger
from ..shared.utils import ensure_instance


class Engine:
    _model_type: type = LanguageModel
    """
    The engine class to run the model.

    :param database: The geoh5py object or group to use as input.
    :param model: The language model to use.
    """

    def __init__(self, database: Database, model: LanguageModel):
        self._database: Database = ensure_instance("database", database, Database)
        self._model: LanguageModel = ensure_instance("model", model, self._model_type)

    @staticmethod
    def _prepare_name(name: str, application_name: str) -> str:
        """
        Prepare the name of the text to add to the database.

        :param name: The name of the text.
        :param application_name: The name of the application.

        :return: The new name
        """
        name = (
            str(name) + "_" + application_name + "_" + pd.Timestamp.now().strftime("%c")
        )
        name = name.replace(" ", "_").replace(":", "_")

        return name

    @property
    def model(self):
        """
        The model of the engine.
        """
        return self._model

    @property
    def database(self) -> Database:
        """
        The database of the engine.
        """
        return self._database


class SynthesizerEngine(Engine):
    """
    The engine class to run the synthesizer model.

    The synthesizer can do a summary
    or answer a question from a text series.
    """

    _model_type = Inquirer

    def __init__(self, database: Database, model: LanguageModel):
        self._model: Inquirer

        super().__init__(database, model)

    def ask(
        self,
        question: str,
        column: str,
        tokens_answer: int,
    ) -> str:
        """
        Ask a question to the model.

        :param question: The question to ask.
        :param column: The column to use.
        :param tokens_answer: The number of tokens to answer the question.
        """
        series: pd.Series = self.database.get_column(column)

        answer, metadata = self.model.ask(
            question,
            series,
            tokens_answer=tokens_answer,
        )

        answer = question + "\n\n" + answer

        name = self._prepare_name(str(series.name), "answer")

        self.database.add_text(name, answer, metadata)

        return name

    def summarize(self, column: str, tokens_resize: int) -> str:
        """
        Summarize the column.

        :param column: The column of the Database to summarize.
        :param max_tokens: The maximum number of tokens to generate.
        :param tokens_resize: The number of tokens to resize the text.
        """
        series: pd.Series = self.database.get_column(column)

        summary, metadata = self.model.summarize(
            series,
            tokens_resize=tokens_resize,
        )

        summary = 'Summary of "' + str(series.name) + '"\n\n' + summary

        name = self._prepare_name(str(series.name), "summary")

        self.database.add_text(name, summary, metadata)

        return name


class ReloggerEngine(Engine):
    """
    The engine class to run the relogger model.

    The relog assign a categorical value to a text,
    for every value of a text series.
    """

    _model_type = Relogger

    def __init__(self, database: Database, model: Relogger):
        self._model: Relogger
        super().__init__(database, model)

    def relog(self, column: str) -> str:
        """
        Relog the column.

        :param column: The column of the Database to relog.
        """
        series: pd.Series = self.database.get_column(column)

        association = self.database.get_association_from_name(column)

        name = self._prepare_name(str(series.name), "relogged")

        relogged, metadata = self.model.relog(series)
        relogged.name = name

        self._database.add_data(relogged, association, metadata, self.model.classes)

        return name
