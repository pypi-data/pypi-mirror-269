import os

from prometheus_client import Counter, Gauge

from matter_observability.config import Config

if os.getenv("INSTANCE_TYPE") == "celery":
    from .utils import REGISTRY
else:
    from prometheus_client import REGISTRY


GAUGE_PROCESSING_TIME = Gauge(
    f"{Config.INSTANCE_NAME.lower().replace('-','_')}_processing_time",
    f"Processing time in {Config.INSTANCE_NAME.capitalize()}",
    labelnames=["action"],
    registry=REGISTRY,
)

GAUGE_CUSTOM = Gauge(
    f"{Config.INSTANCE_NAME.lower().replace('-','_')}_gauge",
    f"Gauge a parameter in {Config.INSTANCE_NAME.capitalize()}",
    labelnames=["parameter"],
    registry=REGISTRY,
)

COUNTER_CUSTOM = Counter(
    f"{Config.INSTANCE_NAME.lower().replace('-','_')}_number_of_occurrences",
    f"Total {Config.INSTANCE_NAME.capitalize()} Count",
    labelnames=["counter"],
    registry=REGISTRY,
)
