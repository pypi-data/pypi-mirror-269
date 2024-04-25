from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .request_id import process_request_id


def configure_middleware(app: FastAPI, skip_paths: list[str] | None = None) -> None:
    metrics_path = "/internal/metrics"
    skip_paths = skip_paths or [metrics_path]

    app.middleware("http")(process_request_id)

    Instrumentator(excluded_handlers=skip_paths, should_respect_env_var=True, env_var_name="ENABLE_METRICS").instrument(
        app=app
    ).expose(app=app, endpoint=metrics_path)
