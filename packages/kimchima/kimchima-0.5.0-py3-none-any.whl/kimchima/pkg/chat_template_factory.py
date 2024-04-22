# coding=utf-8
# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from kimchima.pkg import logging


logger=logging.get_logger(__name__)

class ChatTemplateFactory:
    r"""
    A factory class for creating prompt from chat Template for different ML tasks.
    """

    def __init__(self):
        raise EnvironmentError(
            "Chat Template is designed to be instantiated "
        )

    @classmethod
    def prompt_generation(cls, *args,**kwargs)-> list[int]:
        r"""
        Create prompt by using the Huggingface Transformers library.
        """
        messages=kwargs.pop("messages", None)
        if messages is None:
            raise ValueError("messages is required")
        tokenizer=kwargs.pop("tokenizer", None)
        if tokenizer is None:
            raise ValueError("tokenizer is required")

        tokenize=kwargs.pop("tokenize", False)
        add_generation_prompt=kwargs.pop("add_generation_prompt", False)

        tokenized_chat  = tokenizer.apply_chat_template(messages, tokenize=tokenize, add_generation_prompt=add_generation_prompt)

        return tokenized_chat
