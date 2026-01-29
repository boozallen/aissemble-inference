###
# #%L
# aiSSEMBLE::Open Inference Protocol::Modules::sumy
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
"""Sumy-specific translator for text summarization.

This module provides a translator optimized for sumy library outputs.
Currently uses the default summarization translator from core,
but can be extended with sumy-specific optimizations if needed.
"""

from aissemble_inference_core.client.translators import DefaultSummarizationTranslator


class SumyTranslator(DefaultSummarizationTranslator):
    """Translator for sumy summarization models.

    This translator handles the standard text summarization format:
    - Input: Plain text string
    - Output: Summarized text string

    Currently inherits all behavior from DefaultSummarizationTranslator.
    Can be extended with sumy-specific preprocessing or postprocessing
    if needed (e.g., text cleaning, sentence segmentation).
    """

    pass
