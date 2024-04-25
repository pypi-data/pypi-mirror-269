# sparkle_log

Write a spark line graph of CPU, Memory, etc to the python log

```text
❯ sparkle_log
Demo of Sparkle Monitoring system metrics during operations...
INFO     CPU   :   % |                              ▄ | min, mean, max (4, 4, 4)
INFO     Memory:   % |                              ▄ | min, mean, max (46, 46, 46)
Maybe CPU intensive work done here...
INFO     CPU   :   % |                           ▆▁█▄ | min, mean, max (1, 3.2, 5)
INFO     Memory:   % |                           ▄▄▄▄ | min, mean, max (46, 46, 46)
Maybe Memory intensive work done here...
INFO     Memory:   % |                         ▄▄▄▄▄▄ | min, mean, max (46, 46, 46)
INFO     CPU   :   % |                        ▆▁█▄▃▃▁ | min, mean, max (1, 2.6, 5)
INFO     Memory:   % |                        ▄▄▄▄▄▄▄ | min, mean, max (46, 46, 46)
```

## Install

`pip install sparkle_log`

## Usage

This will write up to log entries to your AWS Lambda log, at a frequency you specify, e.g. every 60 seconds.
Light-weight, cheap, immediately correlates to your other print statements and log entries.

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

You could also use container insights or htop. This tool should provide the most value when the server is headless and
you only have logging or no easy way to correlate log entries to graphs.
