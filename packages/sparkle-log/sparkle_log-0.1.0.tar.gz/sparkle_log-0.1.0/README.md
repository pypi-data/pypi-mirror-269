# sparkle_log
Write a spark line graph of CPU, Memory, etc to the python log


## Install

`pip install sparkle_log`


## Usage

This will write up to 15 log entries to your AWS Lambda log, one per minute. Very light-weight, cheap, immediately 
correlates to your other print statements and log entries.

If logging is less than INFO, then no data is collected.

As a decorator
```python
import sparkle_log
import logging

logging.basicConfig(level=logging.INFO)


@sparkle_log.monitor_metrics_on_call(("cpu", "memory"), 60)
def handler_name(event, context) -> str:
    return "Hello world!"
```

As a context manager:
```python
import time
import sparkle_log
import logging

logging.basicConfig(level=logging.INFO)


def handler_name(event, context) -> str:
    with sparkle_log.MetricsLoggingContext(metrics=("cpu", "memory"), interval=5):
        time.sleep(20)
        return "Hello world!"
```


## Prior art
You could also use container insights or htop. This tool should provide the most value when the server is headless 
and you only have logging or no easy way to correlate log entries to graphs.