from dataclasses import dataclass
import numpy
import numpy.random
import typing
from enum import Enum
from tantri.dipoles.types import DipoleTO

import logging

_logger = logging.getLogger(__name__)


class DipoleMeasurementType(Enum):
	ELECTRIC_POTENTIAL = 1
	X_ELECTRIC_FIELD = 2


@dataclass(frozen=True)
class DotPosition:
	# assume len 3
	r: numpy.ndarray
	label: str


@dataclass
class WrappedDipole:
	# assumed len 3
	p: numpy.ndarray
	s: numpy.ndarray

	# should be 1/tau up to some pis
	w: float

	# For caching purposes tell each dipole where the dots are
	# TODO: This can be done better by only passing into the time series the non-repeated p s and w,
	# TODO: and then creating a new wrapper type to include all the cached stuff.
	# TODO: Realistically, the dot positions and measurement type data should live in the time series.
	dot_positions: typing.Sequence[DotPosition]

	measurement_type: DipoleMeasurementType

	def __post_init__(self) -> None:
		"""
		Coerce the inputs into numpy arrays.
		"""
		self.p = numpy.array(self.p)
		self.s = numpy.array(self.s)

		self.state = 1
		self.cache = {}
		for pos in self.dot_positions:
			if self.measurement_type is DipoleMeasurementType.ELECTRIC_POTENTIAL:
				self.cache[pos.label] = self.potential(pos)
			elif self.measurement_type is DipoleMeasurementType.X_ELECTRIC_FIELD:
				self.cache[pos.label] = self.e_field_x(pos)

	def potential(self, dot: DotPosition) -> float:
		# let's assume single dot at origin for now
		r_diff = self.s - dot.r
		return self.p.dot(r_diff) / (numpy.linalg.norm(r_diff) ** 3)

	def e_field_x(self, dot: DotPosition) -> float:
		# let's assume single dot at origin for now
		r_diff = self.s - dot.r
		norm = numpy.linalg.norm(r_diff)

		return (
			((3 * self.p.dot(r_diff) * r_diff / (norm**2)) - self.p) / (norm**3)
		)[0]

	def transition(
		self, dt: float, rng_to_use: typing.Optional[numpy.random.Generator] = None
	) -> typing.Dict[str, float]:
		rng: numpy.random.Generator
		if rng_to_use is None:
			rng = numpy.random.default_rng()
		else:
			rng = rng_to_use
		# if on average flipping often, then just return 0, basically this dipole has been all used up.
		# Facilitates going for different types of noise at very low freq?
		if dt * 10 >= 1 / self.w:
			# _logger.warning(
			# 	f"delta t {dt} is too long compared to dipole frequency {self.w}"
			# )
			self.state = rng.integers(0, 1, endpoint=True)
		else:
			prob = dt * self.w
			if rng.random() < prob:
				# _logger.debug("flip!")
				self.flip_state()
		return {k: self.state * v for k, v in self.cache.items()}

	def flip_state(self):
		self.state *= -1


def get_wrapped_dipoles(
	dipole_tos: typing.Sequence[DipoleTO],
	dots: typing.Sequence[DotPosition],
	measurement_type: DipoleMeasurementType,
) -> typing.Sequence[WrappedDipole]:
	return [
		WrappedDipole(
			p=dipole_to.p,
			s=dipole_to.s,
			w=dipole_to.w,
			dot_positions=dots,
			measurement_type=measurement_type,
		)
		for dipole_to in dipole_tos
	]


class DipoleTimeSeries:
	def __init__(
		self,
		dipoles: typing.Sequence[DipoleTO],
		dots: typing.Sequence[DotPosition],
		measurement_type: DipoleMeasurementType,
		dt: float,
		rng_to_use: typing.Optional[numpy.random.Generator] = None,
	):
		self.rng: numpy.random.Generator
		if rng_to_use is None:
			self.rng = numpy.random.default_rng()
		else:
			self.rng = rng_to_use

		self.dipoles = get_wrapped_dipoles(dipoles, dots, measurement_type)
		self.state = 0
		self.dt = dt

	def transition(self) -> typing.Dict[str, float]:
		new_vals = [dipole.transition(self.dt, self.rng) for dipole in self.dipoles]

		ret = {}
		for transition in new_vals:
			for k, v in transition.items():
				if k not in ret:
					ret[k] = v
				else:
					ret[k] += v
		return ret


__all__ = [
	"WrappedDipole",
	"DipoleTimeSeries",
	"DipoleTO",
]
