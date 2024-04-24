import logging
import statistics

import psutil

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

READINGS: dict[str, list[int]] = {"cpu": [], "memory": []}


def log_system_metrics(metrics: tuple[str, ...]) -> None:
    if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
        return
    if "cpu" in metrics:
        # Interval non to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = psutil.cpu_percent(interval=interval)

        if reading == 0 and interval is None:
            # First reading on interval None is trash, bail.
            return
        READINGS["cpu"].append(int(reading))
    if "memory" in metrics:
        READINGS["memory"].append(int(psutil.virtual_memory().percent))

    for _key, value in READINGS.items():
        if len(value) > 30:  # Keep the last 30 readings
            value.pop(0)

    for metric, value in READINGS.items():
        if metric not in metrics:
            continue
        average = round(statistics.mean(value), 1)
        minimum = min(value)
        maximum = max(value)
        if metric == "cpu":
            GLOBAL_LOGGER.info(
                f"CPU: {value[-1]}% | {sparkline(value)} | min, mean, max ({minimum}, {average}, {maximum})"
            )
        elif metric == "memory":
            GLOBAL_LOGGER.info(
                f"Memory: {value[-1]}% | {sparkline(value)} | min, mean, max ({minimum}, {average}, {maximum})"
            )
