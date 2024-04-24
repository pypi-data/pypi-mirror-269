import functools
from asyncio import iscoroutinefunction

from .custom_metrics import COUNTER_CUSTOM, GAUGE_CUSTOM, GAUGE_PROCESSING_TIME
from .labeled_counter import LabeledCounter
from .labeled_gauge import LabeledGauge
from .labeled_gauge_duration import LabeledGaugeDuration


def gauge_value(label: str, use_push_gateway: bool = False):
    labeled_gauge = LabeledGauge(use_push_gateway=use_push_gateway, metric=GAUGE_CUSTOM, label=label)

    def wrapped(func):
        @functools.wraps(func)
        async def execute_async(*arg, **kwargs):
            return await func(*arg, **kwargs, gauge=labeled_gauge)

        @functools.wraps(func)
        def execute(*arg, **kwargs):
            return func(*arg, **kwargs, gauge=labeled_gauge)

        if iscoroutinefunction(func):
            return execute_async
        return execute

    return wrapped


def measure_processing_time(label: str, use_push_gateway: bool = False):
    labeled_processing_time = LabeledGaugeDuration(
        use_push_gateway=use_push_gateway, metric=GAUGE_PROCESSING_TIME, label=label
    )

    def wrapped(func):
        @functools.wraps(func)
        async def execute_async(*arg, **kwargs):
            labeled_processing_time.start()
            try:
                return await func(*arg, **kwargs)
            finally:
                labeled_processing_time.stop()

        @functools.wraps(func)
        def execute(*arg, **kwargs):
            labeled_processing_time.start()
            try:
                return func(*arg, **kwargs)
            finally:
                labeled_processing_time.stop()

        if iscoroutinefunction(func):
            return execute_async
        return execute

    return wrapped


def count_occurrence(label: str, use_push_gateway: bool = False):
    labeled_counter = LabeledCounter(use_push_gateway=use_push_gateway, metric=COUNTER_CUSTOM, label=label)

    def wrapped(func):
        @functools.wraps(func)
        async def execute_async(*arg, **kwargs):
            try:
                return await func(*arg, **kwargs)
            finally:
                labeled_counter.inc()

        @functools.wraps(func)
        def execute(*arg, **kwargs):
            try:
                return func(*arg, **kwargs)
            finally:
                labeled_counter.inc()

        if iscoroutinefunction(func):
            return execute_async
        return execute

    return wrapped
