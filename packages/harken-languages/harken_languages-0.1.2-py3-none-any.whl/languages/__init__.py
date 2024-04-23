import sys

from funcy import lcat

from .languages import *

modules = ("languages",)
__all__ = lcat(sys.modules["languages." + m].__all__ for m in modules)

