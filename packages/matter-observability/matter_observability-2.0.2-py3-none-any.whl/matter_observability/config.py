import os


class Config:
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"  # Used by prometheus-fastapi-instrumentator
    SERVER_LOG_LEVEL = os.getenv("SERVER_LOG_LEVEL", "info")
    PROMETHEUS_PUSH_GATEWAY_HOST = os.getenv("PROMETHEUS_PUSH_GATEWAY_HOST")
    INSTANCE_NAME = os.getenv("INSTANCE_NAME")
