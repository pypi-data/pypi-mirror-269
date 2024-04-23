import logging
from tantri.meta import __version__
from tantri.simple_telegraph import SimpleTelegraphTimeSeries


def get_version():
	return __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
	"SimpleTelegraphTimeSeries",
	"__version__",
	"get_version",
]
