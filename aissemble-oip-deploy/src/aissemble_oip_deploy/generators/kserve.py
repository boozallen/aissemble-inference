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
KServe deployment generator.

Generates KServe InferenceService configurations for deploying MLServer-based models.
Produces a ServingRuntime (shared runtime configuration) and InferenceService
(model deployment) following the DRY principle.
"""

from pathlib import Path

from .base import Generator, ModelInfo


class KServeGenerator(Generator):
    """Generator for KServe InferenceService deployments."""

    name = "kserve"

    def generate(self, models: list[ModelInfo] | None = None) -> list[Path]:
        """
        Generate KServe deployment configs (ServingRuntime + InferenceService).

        Args:
            models: Models to generate configs for (auto-detected if None)

        Returns:
            List of paths to generated files
        """
        if models is None:
            models = self.detect_models()

        generated_files = []
        target_dir = self.output_dir / "kserve"

        # Extract runtime packages for documentation
        runtime_packages = self.extract_runtime_packages(models)

        # Get image name (consistent with Docker generator)
        image_name = self.get_image_name()

        # Common template context
        context = {
            "models": models,
            "runtime_packages": runtime_packages,
            "image_name": image_name,
            "app_name": image_name,
            "http_port": 8080,
            "grpc_port": 8081,
        }

        # Generate ServingRuntime (shared runtime configuration)
        runtime_content = self.render_template(
            "kserve/serving-runtime.yaml.j2", context
        )
        runtime_path = self.write_file(
            target_dir / "serving-runtime.yaml", runtime_content
        )
        generated_files.append(runtime_path)

        # Generate InferenceService (references the ServingRuntime)
        isvc_content = self.render_template("kserve/inference-service.yaml.j2", context)
        isvc_path = self.write_file(target_dir / "inference-service.yaml", isvc_content)
        generated_files.append(isvc_path)

        # Generate README
        readme_content = self.render_template("kserve/README.md.j2", context)
        readme_path = self.write_file(target_dir / "README.md", readme_content)
        generated_files.append(readme_path)

        return generated_files
