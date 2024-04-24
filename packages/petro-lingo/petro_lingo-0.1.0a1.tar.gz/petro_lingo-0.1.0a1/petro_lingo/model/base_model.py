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

from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict

from ..shared.utils import ensure_instance
from .user import User


class LanguageModelParams(BaseModel):
    """
    The ChatGPTParams class.

    The chat_kwargs are both dependent of the model and its usage and have to be dynamically set.

    :param char_per_token: the approximate number of characters in a string to form a token.
    :param max_tokens_input: the maximum number of tokens the model can receive.
    :param max_tokens_output: the maximum number of tokens the model can return.
    :param user: the user of the model, defining the prompt and the specialization of the model.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    char_per_token: int
    max_tokens_input: int
    max_tokens_output: int
    user: User


class LanguageModel(ABC):
    """
    The base class for all the language model.

    :param params: The parameters of the model.
    """

    _params_type: type = LanguageModelParams

    def __init__(
        self,
        params: LanguageModelParams,
    ):
        self._params: LanguageModelParams = ensure_instance(
            "params", params, self._params_type
        )

    def _count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the text.

        :param text: the text to count the tokens.

        :return: the number of tokens.
        """
        return len(text) // self._params.char_per_token

    @abstractmethod
    def _prompt(self, content: str):
        """
        Prepare the prompt to send to the model.

        :param content: the text to send to the model.

        :return: the prompt to send to the model.
        """

    @abstractmethod
    def _chat(
        self,
        prompt: list[dict],
        max_tokens: int,
        temperature: float,
    ) -> str:
        """
        Run the model with the prompt and return the answer.

        :param prompt: the prompt to send to the model.
        :param max_tokens: the maximum number of tokens to generate.
        :param temperature: the "creativity" of the model, between 0 and 1.

        :return: the answer of the model.
        """

    @property
    def params(self) -> LanguageModelParams:
        """
        The parameters of the model.
        """
        return self._params

    def tokens_available(self, text: str, verify: bool = True) -> int:
        """
        The number of tokens available for the model.

        It returns the number of tokens available for the model to use,
        based on the user's role.
        And raises an error if the prompt is too long.

        :param text: the text to send to the model.
        :param verify: if the prompt length should be verified.

        :return: the number of tokens available.
        """

        prompt_length = (
            self.params.max_tokens_input
            - self.params.max_tokens_output
            - self._count_tokens(self.user.role)
            - self._count_tokens(text)
        )

        if verify and prompt_length <= 0:
            raise ValueError(
                "The prompt is too long by "
                f"{abs(prompt_length - 1)} "
                "tokens, please reduce the prompt or the question."
            )

        return prompt_length

    @property
    def user(self) -> User:
        """
        The model setter change the user of the model only. The engine is not changed.
        """
        return self.params.user

    @user.setter
    def user(self, user: User):
        self.params.user = user
