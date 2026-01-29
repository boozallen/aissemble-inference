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
"""aiSSEMBLE OIP Sumy Module.

This module provides sumy library integration for text summarization
support in the aiSSEMBLE Open Inference Protocol library.

Supported summarization algorithms:
- TextRank: Graph-based ranking algorithm (default)
- LSA: Latent Semantic Analysis
- LexRank: Graph-based ranking with cosine similarity

Usage:
    # Install the module
    pip install aissemble-inference-sumy

    # The module registers itself via entry points
    # InferenceClient will automatically discover it

Example MLServer configuration (model-settings.json):
    {
        "name": "sumy",
        "implementation": "aissemble_inference_sumy.SumyRuntime",
        "parameters": {
            "algorithm": "textrank",
            "sentences_count": 3,
            "language": "english"
        }
    }
"""

from aissemble_inference_sumy.runtime import SumyRuntime
from aissemble_inference_sumy.translator import SumyTranslator

__all__ = ["SumyRuntime", "SumyTranslator"]
