"""Common variables."""
import os
import posixpath

server_url = None

active_run_stack = []
active_experiment_name = None

EXPERIMENT_NAME_FOR_EXECUTOR = "executors"
EXPERIMENT_NAME_FOR_DATASET_LOADER = "dataset_loaders"
FILENAME_FOR_INFERENCE_CONFIG = "predict_config.json"


def _get_server_ml_api() -> str:
    """Get server '/mlflow' endpoint URL."""
    return posixpath.join(_get_server_url(), "mlflow")


def _get_server_url() -> str:
    """
    Get server URL.

    If you set the URL using 'mlmanagement.set_server_url' function,
    it takes precedence over the URL from the environment variable 'server_url'
    """
    return os.environ.get("server_url", "https://local.tai-dev.intra.ispras.ru") if not server_url else server_url
