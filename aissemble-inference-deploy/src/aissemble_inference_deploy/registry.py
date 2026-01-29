###
# #%L
# aiSSEMBLE::Open Inference Protocol::Deploy
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
"""
Generator registry with entry point discovery.

Allows custom generators to be registered via Python entry points,
enabling extensibility for air-gapped systems, custom platforms, etc.
"""

import sys
import threading
from importlib.metadata import entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generators.base import Generator


class GeneratorRegistry:
    """
    Registry for deployment generators discovered via entry points.

    Generators register themselves via the 'inference.generators' entry point group:

        [project.entry-points."inference.generators"]
        openshift = "my_package:OpenShiftGenerator"

    This allows custom generators to be installed as separate packages
    without modifying the core aissemble-inference-deploy module.
    """

    _instance: "GeneratorRegistry | None" = None
    _lock = threading.Lock()

    def __init__(self):
        self._generators: dict[str, type["Generator"]] | None = None

    @classmethod
    def instance(cls) -> "GeneratorRegistry":
        """Get the singleton registry instance (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check locking
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        with cls._lock:
            cls._instance = None

    def _discover_generators(self) -> dict[str, type["Generator"]]:
        """Discover generators from entry points."""
        # Import here to avoid circular imports
        from .generators.base import Generator

        generators: dict[str, type["Generator"]] = {}

        try:
            eps = entry_points(group="inference.generators")
        except Exception as e:
            # entry_points() failed - likely environment issue
            print(
                f"Warning: Failed to discover generators: {e}",
                file=sys.stderr,
            )
            return generators

        for ep in eps:
            try:
                generator_cls = ep.load()

                # Validate it's actually a Generator subclass
                if not isinstance(generator_cls, type):
                    print(
                        f"Warning: Generator '{ep.name}' is not a class: {type(generator_cls)}",
                        file=sys.stderr,
                    )
                    continue

                if not issubclass(generator_cls, Generator):
                    print(
                        f"Warning: Generator '{ep.name}' must be a subclass of Generator, got {generator_cls.__name__}",
                        file=sys.stderr,
                    )
                    continue

                generators[ep.name] = generator_cls

            except ImportError as e:
                print(
                    f"Warning: Failed to import generator '{ep.name}': {e}",
                    file=sys.stderr,
                )
            except Exception as e:
                print(
                    f"Warning: Failed to load generator '{ep.name}': {e}",
                    file=sys.stderr,
                )

        return generators

    @property
    def generators(self) -> dict[str, type["Generator"]]:
        """Get all available generators (lazy-loaded)."""
        if self._generators is None:
            self._generators = self._discover_generators()
        return self._generators

    def get(self, name: str) -> type["Generator"] | None:
        """Get a generator by name, or None if not found."""
        return self.generators.get(name)

    def list_available(self) -> list[str]:
        """List names of all available generators."""
        return sorted(self.generators.keys())

    def register(self, name: str, generator_cls: type["Generator"]) -> None:
        """
        Manually register a generator (useful for testing or runtime registration).

        Args:
            name: The target name (e.g., 'docker', 'kubernetes')
            generator_cls: The generator class

        Raises:
            TypeError: If generator_cls is not a Generator subclass
        """
        from .generators.base import Generator

        if not isinstance(generator_cls, type) or not issubclass(
            generator_cls, Generator
        ):
            raise TypeError(
                f"generator_cls must be a subclass of Generator, got {type(generator_cls)}"
            )

        if self._generators is None:
            self._generators = self._discover_generators()
        self._generators[name] = generator_cls
