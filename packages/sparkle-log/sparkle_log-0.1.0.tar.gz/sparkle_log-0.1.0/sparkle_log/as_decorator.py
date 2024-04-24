import logging
from functools import wraps
from threading import Event, Thread

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler

INITIALIZED = False


def monitor_metrics_on_call(metrics=("cpu", "memory"), interval=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
                return func(*args, **kwargs)
            stop_event = Event()
            scheduler_thread = Thread(target=run_scheduler, args=(stop_event, metrics, interval))
            scheduler_thread.start()

            try:
                return func(*args, **kwargs)
            finally:
                # Stop the scheduler and wait for thread to finish
                stop_event.set()

                scheduler_thread.join()

        return wrapper

    return decorator
