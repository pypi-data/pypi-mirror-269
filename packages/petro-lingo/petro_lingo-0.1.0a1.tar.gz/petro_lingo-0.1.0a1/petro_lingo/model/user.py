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

from pydantic import BaseModel


class User(BaseModel):
    """
    Class to define the user type for prompt engineering.

    :param role: Defines a context for the type of end-user.
    :param summary: Specify the form of the answer.
    """

    role: str
    summary: str


class Geologist(User):
    """
    The geologist user.
    """

    role: str = (
        "As a geologist in mineral industry contexts, "
        "your objective is to derive in-depth geological insights from descriptions. "
        "Responses should be clear, precise, concise, technically detailed, emphasizing "
        "geological intricacies, with appropriate terminology. Do not give interpretation."
    )

    summary: str = (
        "Provide a cohesive geological overview from the text below. "
        "The text provided is segmented into multiple descriptions or paragraphs due "
        "to token limitations. Each paragraphs contains a portion of the overall content. "
        "Consider all parts as a single cohesive unit, focusing on extracting key "
        "geological features and trends. Emphasize key features and trends, "
        "and distill crucial geological information without repetition.\n\n"
    )
