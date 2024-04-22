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

from kimchima.pkg import ModelFactory


@unittest.skip("skip TestModelFactory")
class TestModelFactory(unittest.TestCase):
    model_name = 'gpt2'

    def test_auto_model(self):
        """
        Test auto_model method
        """
        model = ModelFactory.auto_model(pretrained_model_name_or_path=self.model_name)

        # model is not None
        self.assertIsNotNone(model)
        self.assertEqual(model.config.model_type, 'gpt2')

    def test_auto_model_for_causal_lm(self):
        """
        Test auto_model_for_causal_lm method
        """
        model = ModelFactory.auto_model_for_causal_lm(pretrained_model_name_or_path=self.model_name)

        # model is not None
        self.assertIsNotNone(model)
        self.assertEqual(model.config.model_type, 'gpt2')


    def test_model_for_seq2seq(self):
        """
        Test model_for_seq2seq method
        """
        model = ModelFactory.model_for_seq2seq(pretrained_model_name_or_path='google-t5/t5-base')

        # model is not None
        self.assertIsNotNone(model)
        self.assertEqual(model.config.model_type, 't5')
