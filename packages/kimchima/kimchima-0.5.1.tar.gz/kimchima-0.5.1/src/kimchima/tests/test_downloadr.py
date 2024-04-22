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

from kimchima.utils import Downloader
from kimchima.pkg import (
    PipelinesFactory,
    ModelFactory,
    TokenizerFactory
    )


@unittest.skip("skip TestDownloader")
class TestDownloader(unittest.TestCase):
        
        model_name="gpt2"
        folder_name="gpt2"
        model_name_auto="sentence-transformers/all-MiniLM-L6-v2"
        folder_name_auto="encoder"
        

        @classmethod
        def setUpClass(cls):
            r"""
            THe attributes are needed to set up before the test cases are run.
            """
            pass

        
        def test_model_downloader(self):
            """
            Test model_downloader method
            """
            Downloader.save_model_by_pipe(model_name=self.model_name, folder_name=self.folder_name)
            
            # load it from the folder
            pipe=PipelinesFactory.customized_pipe(model=self.folder_name, device_map='auto')

            # pipe is not None
            self.assertIsNotNone(pipe)
            self.assertEqual(pipe.model.name_or_path, self.folder_name)

        
        def test_auto_downloader(self):
            """
            Test auto_downloader method
            """
            Downloader.auto_downloader(model_name=self.model_name_auto, folder_name=self.folder_name_auto)
            Downloader.auto_token_downloader(model_name=self.model_name_auto, folder_name=self.folder_name_auto)
            
            # load it from the folder
            model=ModelFactory.auto_model(pretrained_model_name_or_path=self.folder_name_auto)


            # load it from the local dolder
            tokenizer=TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=self.folder_name_auto)

            self.assertIsNotNone(model)
            self.assertEqual(model.name_or_path, self.folder_name_auto)

            self.assertIsNotNone(tokenizer)

            promt="test"
            input=tokenizer(promt, return_tensors="pt")
            output=model(**input)

            self.assertIsNotNone(output[0])


        def test_casual_downloader(self):
            """
            Test casual_downloader method
            """
            Downloader.casual_downloader(model_name=self.model_name_auto, folder_name=self.folder_name_auto)
            Downloader.auto_token_downloader(model_name=self.model_name_auto, folder_name=self.folder_name_auto)

            model=ModelFactory.auto_model_for_causal_lm(pretrained_model_name_or_path=self.folder_name_auto)
            tokenizer=TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=self.folder_name_auto)

            self.assertIsNotNone(model)
            self.assertEqual(model.name_or_path, self.folder_name_auto)

            self.assertIsNotNone(tokenizer)

            prompt="test"
            input=tokenizer(prompt, return_tensors="pt")
            output=model(**input)
            self.assertIsNotNone(output[0])

            