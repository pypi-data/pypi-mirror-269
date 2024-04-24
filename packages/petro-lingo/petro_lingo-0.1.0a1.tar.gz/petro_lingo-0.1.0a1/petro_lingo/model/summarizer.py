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
from tqdm import tqdm

from ..shared.utils import ensure_instance, prepare_metadata
from .base_model import LanguageModel, LanguageModelParams


class SynthesizerParams(LanguageModelParams):
    """
    The AskParams class.

    :param link: the link to add at the beginning of each paragraph.
    :param temperature: the creativity of the model, can be between 0 and 1.
    """

    link: str = ""
    temperature: float = 0.7


class Summarizer(LanguageModel):
    """
    Class for the summarizer function returning a single text to the user.

    This class it aims to store specific methods for the summarizer
    outside the BaseModel for clarity.
    """

    _params_type = SynthesizerParams

    def _reducing_paragraph(
        self,
        combined_text: list[str],
        question: str,
        tokens_resize: int,
        tokens_limit: int,
    ) -> str:
        """
        Reduce the paragraph to a size that can be pass to the model.

        The text is resized to the token_resize if it exceeds the token_limit.

        :param combined_text: The list of paragraphs to summarize.
        :param question: The question to ask to summarize the text.
        :param tokens_resize: The number of token to resize the text.
        :param tokens_limit: The maximum number of token a text can be.

        :return: The text reduced by the model.
        """
        n_pass = 1
        count = self._count_tokens("\n".join(combined_text))

        while count > tokens_limit:
            # split the text in a list of strings of max token size
            combined_text_list = []
            for paragraph in tqdm(
                combined_text,
                desc=(
                    f"Summarizing - {n_pass} pass - n tokens: "
                    f"{self._count_tokens(''.join(combined_text))}"
                ),
            ):
                sub_summary = self._summarize_paragraph(
                    paragraph,
                    tokens_resize=tokens_resize,
                    question=question,
                )

                combined_text_list.append(sub_summary)

            combined_text = self.divide_paragraphs(
                paragraphs=combined_text_list,
                max_token=tokens_limit,
                token_divide=self.params.char_per_token,
                link=self.params.link,
            )

            previous_count = self._count_tokens("\n".join(combined_text))

            # very unlikely but has to test infinite loop
            if count == previous_count:
                raise ValueError("The text cannot be reduced - infinite loop.")

            count = previous_count
            n_pass += 1

        return "\n".join(combined_text)

    def _summarize_paragraph(
        self, paragraph: str, tokens_resize: int = 500, question: str = ""
    ) -> str:
        """
        Do a summary of the paragraph.

        As it is a private function, the number of tokens must be checked before.

        :param paragraph: The paragraph to summarize.
        :param tokens_resize: The number of token to resize the text.
        :param question: The question to ask to summarize the text.

        :return: the response of the model.
        """
        prompt = self._prompt(
            f"{question}: {paragraph}... \n"
            "Answer in a single paragraph of fewer than "
            f"{int(tokens_resize * (4 / 3) / self._params.char_per_token)} words."
        )

        response = self._chat(
            prompt,
            max_tokens=tokens_resize,
            temperature=self.params.temperature,
        )

        return response

    @staticmethod
    def divide_paragraphs(
        paragraphs: list[str],
        max_token: int,
        token_divide: int,
        link: str = "Descriptions:\n",
    ) -> list:
        """
        Divide the paragraphs in a list of paragraphs of max_token size.

        :param paragraphs: the list of paragraphs to divide.
        :param max_token: the maximum number of token a paragraph can have.
        :param token_divide: the number of token to divide the paragraph.
        :param link: The link to add at the beginning of each paragraph.

        :return: the list of paragraphs.
        """
        count = 0
        paragraphs_list: list = []
        sub_paragraph: list = []

        len_link = len(ensure_instance("link", link, str)) // token_divide + 1

        for paragraph in paragraphs:
            size = len(paragraph) // token_divide
            if size + len_link > max_token:
                for nb_idx in range(0, len(paragraph), max_token * token_divide):
                    paragraphs_list.append(
                        "".join(
                            [
                                link,
                                paragraph[nb_idx : nb_idx + max_token * token_divide],
                            ]
                        )
                    )
                sub_paragraph = []
                count = 0
                continue

            if count + size < max_token:
                sub_paragraph.append("".join([link, paragraph, "\n\n"]))
                count += size + len_link
            else:
                paragraphs_list.append("".join(sub_paragraph))
                sub_paragraph = ["".join([link, paragraph])]
                count = size + len_link

        if len(sub_paragraph) > 0:
            paragraphs_list.append("\n\n".join(sub_paragraph))

        return paragraphs_list

    def summarize(
        self, series: pd.Series, question: str = "", tokens_resize: int = 500
    ) -> tuple[str, dict]:
        """
        Do a summary of the series of text.

        The text in the series are merged together.
        If it exceeds the max_token, the text is resized to the token_resize.

        :param series: the series containing paragraph to summarize.
        :param tokens_resize: the number of token to resize the text.
        :param question: the question to ask to summarize the text.

        :return: the summary of these paragraphs and the metadata.
        """
        if (
            ensure_instance("token_resize", tokens_resize, int)
            >= self.params.max_tokens_output
        ):
            raise ValueError("'tokens_resize' must be inferior to 'max_tokens_output'.")

        # prepare the specific question if needed
        if len(ensure_instance("question", question, str)) > 0:
            question = " ".join(
                [
                    self.user.summary,
                    "Concentrate specifically on aspects related to the question:",
                    ("'" + question + "'"),
                    "\n\n",
                ]
            )
        else:
            question = self.user.summary

        # compute the number of tokens of the question
        tokens_limit = self.tokens_available(
            question + self.user.summary + self.params.link
        )

        # divide the paragraphs in a list of strings of max token size
        combined_text = self.divide_paragraphs(
            ensure_instance("series", series, pd.Series).dropna().tolist(),
            tokens_limit,
            self.params.char_per_token,
            link=self.params.link,
        )

        # reduce the paragraph to a size that can be pass to the model
        distilled_text = self._reducing_paragraph(
            combined_text,
            question,
            tokens_resize,
            tokens_limit,
        )

        # do the summary
        summary = self._summarize_paragraph(
            distilled_text,
            tokens_resize=tokens_resize,
            question=question,
        )

        # prepare the metadata
        params_dict = self.params.dict()
        params_dict.pop("api_key", None)
        metadata = prepare_metadata(
            function="summarize",
            name=str(series.name),
            token_resize=tokens_resize,
            params=params_dict,
            user_profile=self.user.dict(),
        )

        return summary, metadata
