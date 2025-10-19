"""
Draw.io XML generation package for od-draw.

This package provides functionality to generate Draw.io compatible XML files.
It is adapted from the excellent open-source drawpyo package (https://github.com/MerrimanInd/drawpyo)
by Merrimanind, with modifications to support od-draw's multi-backend architecture.

The drawpyo package was used as a starting point because:
- It provides robust Draw.io XML generation
- Well-tested Draw.io format compatibility
- Clean object-oriented design

We've extended and modified it to:
- Add comprehensive type hints
- Simplify for our specific use case (basic shapes only)
- Integrate with od-draw's backend system
- Improve docstrings and documentation
"""

from .file import File
from .page import Page
from .object import Object

__all__ = ["File", "Page", "Object"]
