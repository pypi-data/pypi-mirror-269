import logging
import time
from threading import Event, Thread
from typing import Any, Optional

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler


class MetricsLoggingContext:
    def __init__(self, metrics=("cpu", "memory"), interval: int = 10) -> None:
        if not metrics:
            metrics = ("cpu", "memory")
        else:
            for metric in metrics:
                if metric not in ("cpu", "memory"):
                    raise TypeError("Unexpected metric")
        self.metrics = metrics
        self.interval = interval
        self.stop_event: Optional[Event] = None
        self.scheduler_thread: Optional[Thread] = None

    def __enter__(self) -> "MetricsLoggingContext":
        if GLOBAL_LOGGER.isEnabledFor(logging.INFO):
            self.stop_event = Event()
            self.scheduler_thread = Thread(target=run_scheduler, args=(self.stop_event, self.metrics, self.interval))
            self.scheduler_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.stop_event.set()
            self.scheduler_thread.join()


# Usage example with the context manager
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with MetricsLoggingContext(metrics=("cpu",), interval=1):
        # Execute some operations
        print("Monitoring system metrics during operations...")
        time.sleep(20)
        # Operations are now being monitored
        # The thread will be stopped when exiting this block
