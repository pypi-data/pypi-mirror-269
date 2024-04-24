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

import re
from warnings import warn

import numpy as np
import pandas as pd
from tqdm import tqdm

from ..shared.utils import ensure_instance, prepare_metadata
from .base_model import LanguageModel, LanguageModelParams


class RelogParams(LanguageModelParams):
    """
    The RelogParams class.

    :param batch_size: the number of descriptions to process at once.
    :param intro: the introduction to add at the beginning of the prompt.
    :param tokens_size: the number of tokens to resize the text.
    """

    batch_size: int = 10
    intro: str = ""
    tokens_size: int = 4


class Relogger(LanguageModel):
    """
    Class for the relogging function returning new categories.

    This class it aims to store specific methods for the synthesizer
    outside the BaseModel for clarity.
    """

    _params_type = RelogParams

    def __init__(self, params):
        super().__init__(params)

        self._classes: dict[int, str] | None = None
        self._prompt_classes = None
        self._prompt_tokens = None

    def _ensure_descriptions_length(self, text: list[str]) -> list[str]:
        """
        Ensure the descriptions are not too long.

        This function will cut the descriptions if they are too long.

        :param text: The list of descriptions.

        :return: The list of the descriptions cut if needed.
        """
        # compute the available tokens
        tokens_available = self.tokens_available(self.params.intro)

        tokens_per_prompt = tokens_available // len(text)
        tokens_link = self._count_tokens(self.params.link)

        # reducing descriptions if they are too long
        for idx, description in enumerate(text):
            if self._count_tokens(description) + tokens_link > tokens_per_prompt:
                warn("A description is too long for the prompt, cutting it.")
                text[idx] = description[
                    : tokens_per_prompt * self.params.char_per_token
                ]

        return text

    @staticmethod
    def _ensure_response_length(response: list[int], size: int) -> list[int]:
        """
        Ensure the response is the same length as the input.

        If smaller, fill the response with empty response,
        if bigger, cut the response.

        :param response: The response to ensure the length.
        :param size: The text to compare the length.

        :return: The response with the same length as the input.
        """
        if len(response) != size:
            warn(
                "A response and the input are not the same length, "
                "cutting/filling the response with empty strings."
            )
            response = response + [0] * (size - len(response))

        return response[:size]

    def _extract_class_id(self, text: str) -> list[int]:
        """
        Extract the class ids from the answer of the model.

        :param text: The answer of the model

        :return: The id of the class it corresponds to in a LIST.
        """
        if self.classes is None:
            raise ValueError("The classes are not set.")

        numbers = [int(number) for number in re.findall(r"\d+", text)]

        # Ensure all elements of numbers are in the classes keys
        class_keys = list(set(self.classes.keys()))
        if not all(number in class_keys for number in numbers):
            warn(
                "The response contains a number not in the classes, "
                "replacing it by 0."
            )
            numbers = [0 if number not in class_keys else number for number in numbers]

        return numbers

    def _prepare_prompt(self, text: list[str]) -> list[dict]:
        """
        Prepare the prompt for the model.

        :param text: The text to prepare the prompt for.

        :return: The prompt for the model.
        """
        if self.prompt_classes is None:
            raise ValueError(
                "The 'prompt_classes' is not set."
                "Define the classes to prepare the prompt."
            )

        prompt = self._prompt(
            "".join(
                [
                    self.params.intro,
                    "".join(
                        [
                            f"\n{self.params.link} {idx}:  {txt}"
                            for idx, txt in enumerate(text, start=1)
                        ]
                    ),
                    self.prompt_classes,
                ]
            )
        )

        return prompt

    def _transform_text_to_classes(
        self, text: list[str], tokens_size: int = 10
    ) -> list[int]:
        """
        Transform the text to classes.

        :param text: The text to transform to classes.
        :param tokens_size: The number of tokens to use for the chat.

        :return: The class id.
        """
        if self.classes is None or self.prompt_classes is None:
            raise ValueError("The classes are not set.")

        text = self._ensure_descriptions_length(text)

        prompt = self._prepare_prompt(text)

        response = self._chat(
            prompt, max_tokens=tokens_size, temperature=self.params.temperature
        )

        class_id = self._extract_class_id(response)

        return class_id

    @property
    def classes(self) -> dict[int, str] | None:
        """
        The classes (values) and the ids (keys) of the classes.
        """
        return self._classes

    @classes.setter
    def classes(self, values: list):
        """
        Set the keys to n with the order of the values.

        :param values: the values to set the classes.
        """
        # make sur the values are unique
        values = list(set(ensure_instance("value", values, list)))

        self._classes = {
            idx + 1: ensure_instance(f"value[{idx}]", value, str)
            for idx, value in enumerate(values)
        }

    @property
    def prompt_classes(self) -> str | None:
        """
        Return the prompt for the classes.
        """
        if self._prompt_classes is None and self.classes is not None:
            classes_block = "\n".join(
                [f"{key} - {value}" for key, value in self.classes.items()]
            )

            self._prompt_classes = "".join(
                [
                    "\n\nFor each description above, identify the most likely class "
                    "it belongs to from the list below: \n\n",
                    classes_block,
                    "\n\nRespond with the number of the corresponding classes only, "
                    "separated by commas and in the same order as the input. "
                    "No additional explanation needed.",
                ]
            )
        return self._prompt_classes

    def relog(self, descriptions: pd.Series) -> tuple[pd.Series, dict]:
        """
        Transform the descriptions to classes.

        :param descriptions: The descriptions to transform to classes.

        :return: The classes and the metadata.
        """

        # create an empty pd Series
        classes = pd.Series(
            [0] * len(ensure_instance("descriptions", descriptions, pd.Series)),
            dtype=np.int32,
        )

        # Identify non-empty descriptions
        non_empty_indices = descriptions[descriptions != ""].index

        for idx in tqdm(
            range(0, len(non_empty_indices), self.params.batch_size),
            desc="Relogging",
        ):
            batch_indices = non_empty_indices[idx : idx + self.params.batch_size]

            response = self._transform_text_to_classes(
                descriptions.loc[batch_indices].tolist(), self.params.tokens_size
            )

            classes.loc[batch_indices] = self._ensure_response_length(
                response, len(batch_indices)
            )

        # prepare the metadata
        params_dict = self.params.dict()
        params_dict.pop("api_key", None)
        metadata = prepare_metadata(
            function="relogger",
            name=str(descriptions.name),
            prompt=self.prompt_classes,
            params=params_dict,
            user_profile=self.user.dict(),
        )

        return classes, metadata
