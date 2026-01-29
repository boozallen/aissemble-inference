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
Kubernetes deployment generator.

Generates Kubernetes manifests with Kustomize structure for MLServer deployment.
Includes base manifests and dev/prod overlays for environment-specific configuration.
"""

from pathlib import Path

from .base import Generator, ModelInfo


class KubernetesGenerator(Generator):
    """Generator for Kubernetes deployment configurations using Kustomize."""

    name = "kubernetes"

    def generate(self, models: list[ModelInfo] | None = None) -> list[Path]:
        """
        Generate Kubernetes deployment configs with Kustomize structure.

        Args:
            models: Models to generate configs for (auto-detected if None)

        Returns:
            List of paths to generated files
        """
        if models is None:
            models = self.detect_models()

        generated_files = []
        target_dir = self.output_dir / "kubernetes"

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
            "node_port_http": 30080,
            "node_port_grpc": 30081,
        }

        # Generate base manifests
        base_dir = target_dir / "base"

        deployment_content = self.render_template(
            "kubernetes/deployment.yaml.j2", context
        )
        deployment_path = self.write_file(
            base_dir / "deployment.yaml", deployment_content
        )
        generated_files.append(deployment_path)

        service_content = self.render_template("kubernetes/service.yaml.j2", context)
        service_path = self.write_file(base_dir / "service.yaml", service_content)
        generated_files.append(service_path)

        base_kustomization_content = self.render_template(
            "kubernetes/kustomization.yaml.j2", context
        )
        base_kustomization_path = self.write_file(
            base_dir / "kustomization.yaml", base_kustomization_content
        )
        generated_files.append(base_kustomization_path)

        # Generate dev overlay
        dev_dir = target_dir / "overlays" / "dev"
        dev_kustomization_content = self.render_template(
            "kubernetes/overlays/dev/kustomization.yaml.j2", context
        )
        dev_kustomization_path = self.write_file(
            dev_dir / "kustomization.yaml", dev_kustomization_content
        )
        generated_files.append(dev_kustomization_path)

        # Generate prod overlay
        prod_dir = target_dir / "overlays" / "prod"
        prod_kustomization_content = self.render_template(
            "kubernetes/overlays/prod/kustomization.yaml.j2", context
        )
        prod_kustomization_path = self.write_file(
            prod_dir / "kustomization.yaml", prod_kustomization_content
        )
        generated_files.append(prod_kustomization_path)

        # Generate README
        readme_content = self.render_template("kubernetes/README.md.j2", context)
        readme_path = self.write_file(target_dir / "README.md", readme_content)
        generated_files.append(readme_path)

        return generated_files
