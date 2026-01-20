###
# #%L
# aiSSEMBLE::Open Inference Protocol::Examples::Summarization
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
"""aiSSEMBLE Summarization Example.

This example demonstrates how to use the aissemble-oip-sumy module
for text summarization with MLServer and the OIP Client.

Features demonstrated:
- MLServer integration with SumyRuntime
- InferenceClient fluent API for summarization
- Multiple summarization algorithms (TextRank, LSA, LexRank)
- Parameter configuration (sentences_count, language)
- BDD testing patterns for OIP modules

See README.md for usage instructions.
"""
