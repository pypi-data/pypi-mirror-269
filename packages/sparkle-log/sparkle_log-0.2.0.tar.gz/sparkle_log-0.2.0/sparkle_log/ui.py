"""
Sparkline graph code goes here.
"""

import sparklines


def sparkline(numbers: list[int]) -> str:
    """Generate a simple sparkline string for a list of integers."""
    for line in sparklines.sparklines(numbers):
        return line
    return ""
