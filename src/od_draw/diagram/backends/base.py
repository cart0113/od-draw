"""
Base backend class for od-draw.
"""

from abc import ABC, abstractmethod
from typing import List, Any


class Backend(ABC):
    @abstractmethod
    def render(self, shapes: List[Any], output_path: str, **kwargs):
        pass

    @abstractmethod
    def show(self, shapes: List[Any], **kwargs):
        pass
