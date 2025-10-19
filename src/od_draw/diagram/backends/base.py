"""
Base backend class for od-draw.
"""

from abc import ABC, abstractmethod
from typing import List
from ...shapes.base import Shape


class Backend(ABC):
    @abstractmethod
    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        pass

    @abstractmethod
    def show(self, shapes: List[Shape], **kwargs):
        pass
