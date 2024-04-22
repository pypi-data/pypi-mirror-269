
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


class Dialog:
     
    def __init__(self):
        raise EnvironmentError(
            "Dialog is designed to be instantiated "
            "using the `Dialog.chat_summary()` method."
        )

    @classmethod
    def chat_summary(cls, *args,**kwargs)-> str:
        r"""
        Chat and summarize the conversation.
        """
        pipe_con=kwargs.pop("pipe_con", None)
        if pipe_con is None:
            raise ValueError("conversation pipeline is required")
            
        pipe_sum=kwargs.pop("pipe_sum", None)
        if pipe_sum is None:
            raise ValueError("summarization pipeline is required")
            
        messages=kwargs.pop("messages", None)
        if messages is None:
            raise ValueError("messages is required")

        prompt=kwargs.pop("prompt", None)
        max_length=kwargs.pop("max_length", None)
            
        response = pipe_con(messages)

        logger.info("Finish conversation pipeline")
        if prompt is None:
            return response.messages[-1]["content"]
            
        raw_response = prompt + response.messages[-1]["content"]
            
        if max_length is None:
            max_length = len(raw_response)

        response = pipe_sum(raw_response, min_length=5, max_length=max_length)

        logger.info("Finish summarization pipeline")

        return response[0].get('summary_text')
    
    @classmethod
    def dialog_with_pipe(cls, *args, **kwargs):
        r"""
        Conversational pipeline with the conversation.

        Args:
            * conver_pipe: pipeline with `conversational` task
                * like pipeline(task='conversational',model="microsoft/GODEL-v1_1-base-seq2seq", tokenizer=tokenizer)
            * con: Huggingface transformers Conversation class instance
            * **kwargs:
                * max_length: maximum length of the response
                * min_length: minimum length of the response
                * top_k: top k tokens to sample from
                * top_p: top p tokens to sample from
                * temperature: temperature of the sampling
                * do_sample: whether to sample
        """
        conver_pipe=kwargs.pop("conver_pipe", None)
        if conver_pipe is None:
            raise ValueError("conversation pipeline is required")
        
        con=kwargs.pop("con", None)
        if con is None:
            raise ValueError("con is required")
        
        return conver_pipe(con, **kwargs)
    
    @classmethod
    def summary_with_pipe(cls, *args, **kwargs):
        r"""
        Summary conversaion records with the summarization pipeline.
        """
        summary_pipe=kwargs.pop("summary_pipe", None)
        if summary_pipe is None:
            raise ValueError("summary pipeline is required")

        paragraph=kwargs.pop("paragraph", None)
        if paragraph is None:
            raise ValueError("paragraph is required")

        return summary_pipe(paragraph, **kwargs)


        
