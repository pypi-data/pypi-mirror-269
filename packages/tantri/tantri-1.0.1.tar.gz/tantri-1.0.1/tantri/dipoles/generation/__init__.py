import numpy
from typing import Sequence, Optional
from dataclasses import dataclass, asdict
from tantri.dipoles.types import DipoleTO
from enum import Enum
import logging


# stuff for generating random dipoles from parameters

_logger = logging.getLogger(__name__)


class Orientation(str, Enum):
	# Enum for orientation, making string for json serialisation purposes
	#
	# Note that htis might not be infinitely extensible?
	# https://stackoverflow.com/questions/75040733/is-there-a-way-to-use-strenum-in-earlier-python-versions
	XY = "XY"
	Z = "Z"
	RANDOM = "RANDOM"


# A description of the parameters needed to generate random dipoles
@dataclass
class DipoleGenerationConfig:
	# note no actual checks anywhere that these are sensibly defined with min less than max etc.
	x_min: float
	x_max: float
	y_min: float
	y_max: float
	z_min: float
	z_max: float

	mag: float

	# these are log_10 of actual value
	w_log_min: float
	w_log_max: float

	orientation: Orientation

	dipole_count: int
	generation_seed: int

	def __post_init__(self):
		# This allows us to transparently set this with a string, while providing early warning of a type error
		self.orientation = Orientation(self.orientation)

	def as_dict(self) -> dict:
		return_dict = asdict(self)

		return_dict["orientation"] = return_dict["orientation"].value

		return return_dict


def make_dipoles(
	config: DipoleGenerationConfig,
	rng_override: Optional[numpy.random.Generator] = None,
) -> Sequence[DipoleTO]:

	if rng_override is None:
		_logger.info(
			f"Using the seed [{config.generation_seed}] provided by configuration for dipole generation"
		)
		rng = numpy.random.default_rng(config.generation_seed)
	else:
		_logger.info("Using overridden rng, of unknown seed")
		rng = rng_override

	dipoles = []

	for i in range(config.dipole_count):
		sx = rng.uniform(config.x_min, config.x_max)
		sy = rng.uniform(config.y_min, config.y_max)
		sz = rng.uniform(config.z_min, config.z_max)

		# orientation
		# 0, 1, 2
		# xy, z, random

		if config.orientation is Orientation.RANDOM:
			theta = numpy.arccos(2 * rng.random() - 1)
			phi = 2 * numpy.pi * rng.random()
		elif config.orientation is Orientation.Z:
			theta = 0
			phi = 0
		elif config.orientation is Orientation.XY:
			theta = numpy.pi / 2
			phi = 2 * numpy.pi * rng.random()
		else:
			raise ValueError(
				f"this shouldn't have happened, orientation index: {config}"
			)

		px = config.mag * numpy.cos(phi) * numpy.sin(theta)
		py = config.mag * numpy.sin(phi) * numpy.sin(theta)
		pz = config.mag * numpy.cos(theta)

		w = 10 ** rng.uniform(config.w_log_min, config.w_log_max)

		dipoles.append(
			DipoleTO(numpy.array([px, py, pz]), numpy.array([sx, sy, sz]), w)
		)

	return dipoles
