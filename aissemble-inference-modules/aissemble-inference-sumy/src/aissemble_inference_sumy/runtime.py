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
"""Sumy model family runtime for MLServer.

This module provides an MLServer-compatible runtime that wraps sumy library
summarization algorithms for text summarization inference via the
Open Inference Protocol.
"""

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput


class SumyRuntime(MLModel):
    """MLServer runtime for sumy text summarization.

    Supports multiple summarization algorithms through the sumy library:
    - TextRank: Graph-based ranking algorithm (default)
    - LSA: Latent Semantic Analysis
    - LexRank: Graph-based ranking with cosine similarity

    Configuration via model-settings.json:
        {
            "name": "sumy",
            "implementation": "aissemble_inference_sumy.SumyRuntime",
            "parameters": {
                "algorithm": "textrank",
                "sentences_count": 3,
                "language": "english"
            }
        }

    This runtime accepts text strings and returns summarized text.
    """

    async def load(self) -> bool:
        """Load the summarization model.

        Initializes the specified summarization algorithm, downloads required
        NLTK data (punkt tokenizer), and prepares the runtime for inference.

        Returns:
            True if model loaded successfully

        Raises:
            ValueError: If an unsupported algorithm is specified
        """
        import nltk
        from sumy.nlp.stemmers import Stemmer

        # Download NLTK data if not already present
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)

        # Get configuration parameters
        self._algorithm = self._get_algorithm()
        self._sentences_count = self._get_sentences_count()
        self._language = self._get_language()

        # Create stemmer for the specified language
        self._stemmer = Stemmer(self._language)

        # Create summarizer instance
        self._summarizer = self._create_summarizer(self._algorithm)

        self.ready = True
        return self.ready

    async def health(self) -> dict:
        """Health check endpoint.

        Returns a lightweight health status without running expensive inference.
        This is called by MLServer's `/v2/health/ready` endpoint.

        Returns:
            Health status dict
        """
        return {"status": "ok"}

    def _get_algorithm(self) -> str:
        """Get the algorithm from settings.

        Supports both direct attribute access (for backwards compatibility)
        and extra dict access (MLServer 1.6+ style).

        Returns:
            Algorithm name string, defaults to 'textrank'
        """
        default = "textrank"
        params = self.settings.parameters
        if params is None:
            return default

        # Try direct attribute access first (backwards compatibility)
        if hasattr(params, "algorithm") and params.algorithm is not None:
            return params.algorithm

        # Try extra dict (MLServer 1.6+ style)
        if hasattr(params, "extra") and params.extra:
            return params.extra.get("algorithm", default)

        return default

    def _get_sentences_count(self) -> int:
        """Get the sentences_count from settings.

        Returns:
            Number of sentences in summary, defaults to 3
        """
        default = 3
        params = self.settings.parameters
        if params is None:
            return default

        # Try direct attribute access first
        if hasattr(params, "sentences_count") and params.sentences_count is not None:
            return int(params.sentences_count)

        # Try extra dict
        if hasattr(params, "extra") and params.extra:
            return int(params.extra.get("sentences_count", default))

        return default

    def _get_language(self) -> str:
        """Get the language from settings.

        Returns:
            Language name string, defaults to 'english'
        """
        default = "english"
        params = self.settings.parameters
        if params is None:
            return default

        # Try direct attribute access first
        if hasattr(params, "language") and params.language is not None:
            return params.language

        # Try extra dict
        if hasattr(params, "extra") and params.extra:
            return params.extra.get("language", default)

        return default

    def _create_summarizer(self, algorithm: str):
        """Factory method for sumy summarizer instances.

        Args:
            algorithm: Name of the summarization algorithm

        Returns:
            Initialized summarizer instance

        Raises:
            ValueError: If algorithm is not supported
        """
        from sumy.summarizers.text_rank import TextRankSummarizer
        from sumy.summarizers.lsa import LsaSummarizer
        from sumy.summarizers.lex_rank import LexRankSummarizer

        algorithm_map = {
            "textrank": TextRankSummarizer,
            "lsa": LsaSummarizer,
            "lexrank": LexRankSummarizer,
        }

        if algorithm not in algorithm_map:
            supported = ", ".join(algorithm_map.keys())
            raise ValueError(
                f"Unsupported algorithm: {algorithm}. Supported algorithms: {supported}"
            )

        summarizer_class = algorithm_map[algorithm]
        return summarizer_class(self._stemmer)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """Run summarization on the input text.

        Args:
            payload: OIP inference request with text input

        Returns:
            OIP response with summarized text

        Raises:
            ValueError: If payload is malformed or missing text data
        """
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer

        if not payload.inputs or len(payload.inputs) == 0:
            raise ValueError("Payload must contain at least one input tensor")

        text_input = payload.inputs[0]
        if not text_input.data or len(text_input.data) == 0:
            raise ValueError(f"Input '{text_input.name}' must contain data")

        # Handle both nested [[text]] format and flat [text] format
        if isinstance(text_input.data[0], (list, tuple)):
            text_data = text_input.data[0][0]
        else:
            text_data = text_input.data[0]

        if text_data is None:
            raise ValueError("Text data cannot be None")

        # Decode bytes to string if necessary
        if isinstance(text_data, bytes):
            text = text_data.decode("utf-8")
        else:
            text = str(text_data)

        if not text.strip():
            raise ValueError("Input text cannot be empty")

        # Parse the text
        parser = PlaintextParser.from_string(text, Tokenizer(self._language))

        # Run summarization
        summary_sentences = self._summarizer(parser.document, self._sentences_count)

        # Join sentences back into a single string
        summary = " ".join([str(sentence) for sentence in summary_sentences])

        return InferenceResponse(
            model_name=self.name,
            outputs=[
                ResponseOutput(
                    name="summary",
                    shape=[1],
                    datatype="BYTES",
                    data=[summary],
                )
            ],
        )
