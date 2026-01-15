###
# #%L
# aiSSEMBLE::Open Inference Protocol::Core
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
"""Module registry for dynamic OIP module discovery.

This module provides a registry that discovers and loads OIP modules
via Python entry points. Modules can register:
- Runtimes (MLServer-compatible model runtimes)
- Translators (OIP protocol translators)
- Builders (task-specific inference builders)

Entry point groups:
- oip.runtimes: Model runtime implementations
- oip.translators: Data format translators
- oip.builders: Inference builder implementations
"""

import importlib.metadata
import logging
from typing import Any, Dict, List, Type

logger = logging.getLogger(__name__)


class ModuleRegistry:
    """Registry for dynamically discovered OIP modules.

    This registry uses Python entry points to discover installed modules.
    Modules register themselves by declaring entry points in their
    pyproject.toml files.

    Example pyproject.toml entry points:
        [project.entry-points."oip.runtimes"]
        yolo = "aissemble_oip_yolo:YOLORuntime"

        [project.entry-points."oip.translators"]
        yolo = "aissemble_oip_yolo:YOLOTranslator"

    Usage:
        registry = ModuleRegistry.instance()
        registry.discover()

        # Get a specific runtime
        runtime_class = registry.get_runtime("yolo")

        # List all available modules
        available = registry.list_available()
    """

    _instance: "ModuleRegistry | None" = None

    def __init__(self):
        """Initialize an empty registry."""
        self._runtimes: Dict[str, Type[Any]] = {}
        self._translators: Dict[str, Type[Any]] = {}
        self._builders: Dict[str, Type[Any]] = {}
        self._loaded = False

    @classmethod
    def instance(cls) -> "ModuleRegistry":
        """Get the singleton registry instance.

        Returns:
            The global ModuleRegistry instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (primarily for testing)."""
        cls._instance = None

    def discover(self) -> None:
        """Load all installed OIP modules via entry points.

        This method scans for entry points in the following groups:
        - oip.runtimes: Model runtime implementations
        - oip.translators: Data format translators
        - oip.builders: Inference builder implementations

        Entry points are loaded lazily - the actual class is only
        imported when accessed via get_* methods.
        """
        if self._loaded:
            return

        entry_point_groups = [
            ("oip.runtimes", self._runtimes),
            ("oip.translators", self._translators),
            ("oip.builders", self._builders),
        ]

        for group, registry in entry_point_groups:
            try:
                eps = importlib.metadata.entry_points(group=group)
                for ep in eps:
                    try:
                        registry[ep.name] = ep.load()
                        logger.debug(f"Loaded {group} entry point: {ep.name}")
                    except Exception as e:
                        logger.warning(
                            f"Failed to load {group} entry point '{ep.name}': {e}"
                        )
            except Exception as e:
                logger.warning(f"Failed to scan entry points for group '{group}': {e}")

        self._loaded = True

    def get_runtime(self, name: str) -> Type[Any] | None:
        """Get a runtime class by name.

        Args:
            name: The registered name of the runtime

        Returns:
            The runtime class, or None if not found
        """
        self.discover()
        return self._runtimes.get(name)

    def get_translator(self, name: str) -> Type[Any] | None:
        """Get a translator class by name.

        Args:
            name: The registered name of the translator

        Returns:
            The translator class, or None if not found
        """
        self.discover()
        return self._translators.get(name)

    def get_builder(self, name: str) -> Type[Any] | None:
        """Get a builder class by name.

        Args:
            name: The registered name of the builder

        Returns:
            The builder class, or None if not found
        """
        self.discover()
        return self._builders.get(name)

    def list_available(self) -> Dict[str, List[str]]:
        """List all discovered modules.

        Returns:
            Dictionary mapping category to list of available module names
        """
        self.discover()
        return {
            "runtimes": list(self._runtimes.keys()),
            "translators": list(self._translators.keys()),
            "builders": list(self._builders.keys()),
        }

    def register_runtime(self, name: str, runtime_class: Type[Any]) -> None:
        """Manually register a runtime class.

        Args:
            name: Name to register the runtime under
            runtime_class: The runtime class to register
        """
        self._runtimes[name] = runtime_class

    def register_translator(self, name: str, translator_class: Type[Any]) -> None:
        """Manually register a translator class.

        Args:
            name: Name to register the translator under
            translator_class: The translator class to register
        """
        self._translators[name] = translator_class

    def register_builder(self, name: str, builder_class: Type[Any]) -> None:
        """Manually register a builder class.

        Args:
            name: Name to register the builder under
            builder_class: The builder class to register
        """
        self._builders[name] = builder_class
