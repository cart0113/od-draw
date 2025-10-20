"""
Basic types for od-draw.
"""

from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Size:
    width: float
    height: float
