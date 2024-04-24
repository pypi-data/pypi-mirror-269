import argparse
import logging
import sys
import time
from typing import Optional, Sequence

from sparkle_log.as_context_manager import MetricsLoggingContext
from sparkle_log.as_decorator import monitor_metrics_on_call


@monitor_metrics_on_call(("cpu",), 1)
def log_memory_and_cpu():
    while True:
        time.sleep(4)
        print("Executing demo...")


def log_memory_and_cpu_cli(metrics=("cpu", "memory"), interval: int = 1, duration: int = 20):
    logging.basicConfig(level=logging.INFO)
    with MetricsLoggingContext(metrics=metrics, interval=interval):
        # Execute some operations
        print("Demo of Sparkle Monitoring system metrics during operations...")
        time.sleep(duration)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Monitor system metrics using Sparkle Log.")
    parser.add_argument(
        "--metrics",
        type=str,
        default="cpu,memory",
        help="Comma-separated list of metrics to monitor (e.g., 'cpu,memory')",
    )
    parser.add_argument("--interval", type=int, default=1, help="Interval in seconds between metric logs")
    parser.add_argument("--duration", type=int, default=10, help="Duration in sections to gather metrics")
    parser.add_argument("--version", action="version", version="Sparkle Log 1.0")

    args = parser.parse_args(argv)

    # Convert comma-separated string to tuple of metrics
    metrics_tuple = tuple(args.metrics.split(","))

    # Call the function with parsed arguments
    log_memory_and_cpu_cli(metrics=metrics_tuple, interval=args.interval, duration=args.duration)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
