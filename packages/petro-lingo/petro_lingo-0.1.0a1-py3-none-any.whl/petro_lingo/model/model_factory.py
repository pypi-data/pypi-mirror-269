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

import os

from .base_model import LanguageModel
from .chat_gpt import ChatGPTLanguageModel, ChatGPTParams
from .user import Geologist, User


def model_hangar(model_name: str, application: str) -> dict:
    """
    The model hangar.

    :param model_name: The name of the model to use.
    :param application: The name of the application to use.

    :return: The selected model dictionary.
    """

    models: dict = {
        "gpt-3.5-turbo": {
            "model_class": ChatGPTLanguageModel,
            "param_class": ChatGPTParams,
            "params": {
                "api_key": os.environ.get("OPENAI_API_KEY"),
                "engine_text": "gpt-3.5-turbo",
                "max_tokens_input": 16385,  # see documentation
                "max_tokens_output": 4096,
                "char_per_token": 4,
                "applications": {
                    "synthesize": {"link": "Descriptions:\n", "temperature": 0.1},
                    "relog": {
                        "tokens_size": 50,
                        "temperature": 0.1,
                        "intro": "Based on the description:\n\n",
                    },
                },
            },
        }
    }

    # choose the application to use
    model_params: dict = models[model_name]

    # add the application to the model
    application_parameters: dict = model_params["params"]["applications"].pop(
        application, {}
    )

    # add the application parameters to the model's parameters
    model_params["params"].update(application_parameters)

    return model_params


def user_office(user) -> User:
    """
    The users available.

    :param user: The name of the user to use.

    :return: The selected user.
    """
    return {
        "geologist": Geologist,
    }[user]()


def get_model(model_name: str, application: str, user: str) -> LanguageModel:
    """
    Ride out a model from the hangar with a specific user.

    :param model_name: The name of the model to use.
    :param application: The name of the application to use.
    :param user: The name of User to use.

    :return: The selected Large Language Model.
    """
    model_settings = model_hangar(model_name, application)
    model_settings["params"]["user"] = user_office(user)

    params = model_settings["param_class"](**model_settings["params"])

    model = model_settings["model_class"](params=params)

    return model
