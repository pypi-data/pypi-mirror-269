"""

This is ECV's Python Database Sub Module

"""

__version__ = "0.0.2"
__license__ = "MIT"
__author__ = "Warren Ezra Bruce Jaudian <warren.jaudian@ecloudvalley.com>"

from . import _pynamodb
from .base_model import BaseModel, field

__all__ = ["BaseModel", field]
