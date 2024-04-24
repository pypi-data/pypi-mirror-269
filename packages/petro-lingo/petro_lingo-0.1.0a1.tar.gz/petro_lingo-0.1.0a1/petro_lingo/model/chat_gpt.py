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

import logging

import openai

from .base_model import LanguageModelParams
from .inquirer import Inquirer
from .relogger import Relogger, RelogParams
from .summarizer import SynthesizerParams

logging.getLogger("httpx").setLevel(logging.WARNING)


class ChatGPTParams(SynthesizerParams, RelogParams):
    """
    The ChatGPTParams class.

    :param api_key: the OpenAI API key.
    :param engine_text: the engine to use for text generation.
    """

    api_key: str
    engine_text: str


class ChatGPTLanguageModel(Inquirer, Relogger):
    # pylint: disable=too-few-public-methods
    """
    The ChatGPTLanguageModel class.

    :param params: The parameters of the model.
    """

    def __init__(
        self,
        params=LanguageModelParams,
    ):
        super().__init__(params=params)

        self._client = openai.Client(api_key=self.params.api_key)

    def _prompt(self, content: str) -> list[dict]:
        if len(content) == 0:
            raise TypeError("The content must be a non empty string.")

        prompt = [
            {"role": "system", "content": f"{self.user.role}"},
            {"role": "user", "content": content},
        ]

        return prompt

    def _chat(self, prompt: list, max_tokens: int, temperature: float) -> str:
        """
        Chat with the model.

        :param prompt: The prompt to send to the model.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: The "creativity" of the model, between 0 and 1.

        :return: the response of the model.
        """
        try:
            response = self._client.chat.completions.create(
                model=self.params.engine_text,
                messages=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            return response.choices[0].message.content
        except openai.OpenAIError as error:
            raise ConnectionError(f"OpenAI Error: {error}") from error
