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

import pandas as pd

from ..shared.utils import prepare_metadata
from .summarizer import Summarizer


class Inquirer(Summarizer):
    """
    The Inquirer class to answer a question based on a text.
    """

    def ask(
        self, question: str, words: pd.Series, tokens_answer: int = 200
    ) -> tuple[str, dict]:
        # todo: use Tree of Thought here: https://www.promptingguide.ai/techniques/tot
        """
        Ask a question to the model.

        The question is based on all the paragraph contains in the series

        :param question: the question to ask.
        :param words: the words to use to answer the question.
        :param tokens_answer: the number of tokens to answer the question.

        :return: the answer.
        """
        # summarize the text
        summarized_text, _ = self.summarize(words, question, tokens_answer)

        # prepare the prompt to send to the model
        prompt = (
            f"From the following context: {summarized_text}\n"
            f"answer the question: {question} in fewer than "
            f"{int(tokens_answer * (4 / 3) / self.params.char_per_token)} words."
        )  # super conservative words limit because technical words are token consuming

        # not be possible unless the prompt above is larger than the user's summary
        self.tokens_available(prompt)

        # answer the question
        response = self._chat(
            self._prompt(prompt),
            max_tokens=tokens_answer,
            temperature=self.params.temperature,
        )

        # prepare the metadata
        params_dict = self.params.dict()
        params_dict.pop("api_key", None)
        metadata = prepare_metadata(
            function="ask",
            name=str(words.name),
            question=question,
            tokens_answer=tokens_answer,
            params=params_dict,
            user_profile=self.user.dict(),
        )

        return response, metadata
