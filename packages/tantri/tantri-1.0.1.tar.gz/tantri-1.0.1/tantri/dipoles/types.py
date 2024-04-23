import numpy
from dataclasses import dataclass, asdict


# Lazily just separating this from Dipole where there's additional cached stuff, this is just a thing
# we can use as a DTO For dipole info.
@dataclass
class DipoleTO:
	# assumed len 3
	p: numpy.ndarray
	s: numpy.ndarray

	# should be 1/tau up to some pis
	w: float

	def as_dict(self) -> dict:
		return asdict(self)
