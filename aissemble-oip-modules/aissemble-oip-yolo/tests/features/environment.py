"""Behave environment hooks for YOLO module tests."""

import os
import subprocess
import sys
import tempfile
import time

import requests


def before_all(context):
    """Initialize test context."""
    context.mlserver_process = None
    context.mlserver_url = None
    context.temp_dir = None


def before_scenario(context, scenario):
    """Reset per-scenario state."""
    context.model_variant = None
    context.runtime = None
    context.load_result = None
    context.load_error = None
    context.inference_response = None
    context.inference_error = None
    context.oip_request = None
    context.oip_response = None
    context.detection_result = None
    context.test_image = None
    context.test_image_path = None


def after_scenario(context, scenario):
    """Clean up after each scenario."""
    if context.mlserver_process:
        _stop_mlserver(context)


def after_all(context):
    """Final cleanup."""
    if context.mlserver_process:
        _stop_mlserver(context)
    if context.temp_dir and os.path.exists(context.temp_dir):
        import shutil

        shutil.rmtree(context.temp_dir, ignore_errors=True)


def start_mlserver_with_model(context, model_variant=None):
    """Start MLServer with specified YOLO model configuration.

    Args:
        context: Behave context
        model_variant: Model variant to configure (e.g., "yolov8n.pt")
    """
    if context.mlserver_process:
        _stop_mlserver(context)

    context.temp_dir = tempfile.mkdtemp(prefix="yolo_test_")
    models_dir = os.path.join(context.temp_dir, "models")
    yolo_dir = os.path.join(models_dir, "yolo")
    os.makedirs(yolo_dir)

    settings = {"parallel_workers": 0}
    _write_json(os.path.join(models_dir, "settings.json"), settings)

    model_settings = {
        "name": "yolo",
        "implementation": "aissemble_oip_yolo.YOLORuntime",
    }
    if model_variant:
        model_settings["parameters"] = {"model": model_variant}

    _write_json(os.path.join(yolo_dir, "model-settings.json"), model_settings)

    context.mlserver_port = _find_free_port()
    context.mlserver_url = f"http://localhost:{context.mlserver_port}"

    venv_bin = os.path.dirname(sys.executable)
    mlserver_cmd = os.path.join(venv_bin, "mlserver")

    env = os.environ.copy()
    env["MLSERVER_HTTP_PORT"] = str(context.mlserver_port)
    env["MLSERVER_GRPC_PORT"] = str(context.mlserver_port + 1)
    env["MLSERVER_METRICS_PORT"] = str(context.mlserver_port + 2)

    context.mlserver_process = subprocess.Popen(
        [mlserver_cmd, "start", models_dir],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    _wait_for_server(context.mlserver_url, context.mlserver_process, timeout=120)


def _stop_mlserver(context):
    """Stop MLServer process."""
    if context.mlserver_process:
        context.mlserver_process.terminate()
        try:
            context.mlserver_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            context.mlserver_process.kill()
            context.mlserver_process.wait()
        context.mlserver_process = None


def _wait_for_server(url: str, process: subprocess.Popen, timeout: int = 120):
    """Wait for MLServer to become ready."""
    health_url = f"{url}/v2/health/ready"
    start_time = time.time()

    while time.time() - start_time < timeout:
        exit_code = process.poll()
        if exit_code is not None:
            stdout, stderr = process.communicate()
            raise RuntimeError(
                f"MLServer exited with code {exit_code}.\n"
                f"stdout: {stdout.decode()}\n"
                f"stderr: {stderr.decode()}"
            )

        try:
            response = requests.get(health_url, timeout=2)
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        time.sleep(1)

    process.terminate()
    stdout, stderr = process.communicate(timeout=5)
    raise TimeoutError(
        f"MLServer did not become ready within {timeout} seconds.\n"
        f"stdout: {stdout.decode()}\n"
        f"stderr: {stderr.decode()}"
    )


def _find_free_port():
    """Find a free port to use for MLServer."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def _write_json(path: str, data: dict):
    """Write JSON data to file."""
    import json

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
