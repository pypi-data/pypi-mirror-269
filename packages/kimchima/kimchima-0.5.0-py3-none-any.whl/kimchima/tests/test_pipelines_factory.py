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

import unittest

from kimchima.pkg import (
    ModelFactory,
    TokenizerFactory,
    StreamerFactory,
    PipelinesFactory
)

@unittest.skip("skip TestPipelinesFactory")
class TestPipelinesFactory(unittest.TestCase):
    
        model_name = 'gpt2'
        model=None
        tokenizer=None
        streamer=None
    
        @classmethod
        def setUpClass(cls):
            cls.model = ModelFactory.auto_model_for_causal_lm(pretrained_model_name_or_path=cls.model_name)
            cls.tokenizer = TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=cls.model_name)
            cls.streamer = StreamerFactory.text_streamer(tokenizer=cls.tokenizer)
    
    
        @classmethod
        def tearDownClass(cls):
            pass

        
        def test_cached_pipe(self):
            r"""
            Test the cache mechanism of the pipelines, the second function should not be invoked
            """
            self.assertIsNotNone(self.model)
    
            pipe = PipelinesFactory.text_generation(
                model=self.model,
                tokenizer=self.tokenizer,
                text_streamer=self.streamer
                )
            
            pipe_cached = PipelinesFactory.text_generation(
                model=self.model,
                tokenizer=self.tokenizer,
                text_streamer=self.streamer
                )
            
            # two pipelines should be same obj
            self.assertEqual(pipe, pipe_cached)
            
    
        def test_text_generation(self):
            """
            Test text_generation method
            """
    
            self.assertIsNotNone(self.model)
    
            pipe = PipelinesFactory.text_generation(
                model=self.model,
                tokenizer=self.tokenizer,
                text_streamer=self.streamer
                )
    
            self.assertIsNotNone(pipe)
            self.assertEqual(pipe.task, 'text-generation')


        def test_customized_pipe(self):
            """
            Test customized_pipe method
            """
    
            pipe = PipelinesFactory.customized_pipe(
                task="text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                streamer=self.streamer,
                max_new_tokens=20,
                device_map='auto'
                )
    
            self.assertIsNotNone(pipe)
            self.assertEqual(pipe.task, 'text-generation')

        def test_init_conversation(self):
            """
            Test init_conversation method
            """
            con = PipelinesFactory.init_conversation("how is the weather like in melbourne?")
            con.add_message({"role": "assistant", "content": "The Big lebowski."})
            con.add_message({"role": "user", "content": "Is it good?"})
            self.assertIsNotNone(con)
            self.assertEqual(con.messages[-1]["content"],"Is it good?")