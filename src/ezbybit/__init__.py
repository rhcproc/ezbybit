from importlib.metadata import version

from .client import BybitClient

__version__ = version("ezbybit")

__all__ = ["BybitClient", "__version__"]
