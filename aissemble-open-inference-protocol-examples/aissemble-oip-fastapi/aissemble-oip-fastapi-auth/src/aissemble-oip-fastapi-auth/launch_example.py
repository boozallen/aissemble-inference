###
# #%L
# aiSSEMBLE::Open Inference Protocol FastAPI Examples with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import subprocess
import sys
import shutil


def start_authzforce_docker_container():
    try:
        print("Starting Authzforce container...")
        subprocess.run(
            [
                "curl",
                "-z",
                "server/app.jar",
                "-L",
                "-o",
                "server/app.jar",
                "https://repo1.maven.org/maven2/org/ow2/authzforce/authzforce-ce-restful-pdp-cxf-spring-boot-server/7.1.0/authzforce-ce-restful-pdp-cxf-spring-boot-server-7.1.0.jar",
            ],
            check=True,
        )
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker container: {e}")
        exit(1)


def start_fastapi_with_poetry():
    print("Starting FastAPI app using Poetry...")
    try:
        subprocess.run(
            [
                "poetry",
                "run",
                "fastapi",
                "dev",
                "./src/aissemble-oip-fastapi-auth/main.py",
            ]
        )
    except KeyboardInterrupt:
        subprocess.run(["docker", "compose", "down"], check=False)
        print("Closing FastAPI & Authzforce")


def run_poetry_build():
    try:
        result = subprocess.run(
            ["poetry", "build"], check=True, capture_output=True, text=True
        )
        print("Build succeeded!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Build failed:")
        print(e.stderr)


def check_if_poetry_is_installed():
    if shutil.which("poetry") is None:
        print("Poetry is not installed. Please install it before continuing.")
        sys.exit(1)


if __name__ == "__main__":
    check_if_poetry_is_installed()
    start_authzforce_docker_container()
    run_poetry_build()
    start_fastapi_with_poetry()
