import numpy.random


class SimpleTelegraphTimeSeries:
	def __init__(
		self, rng_to_use: numpy.random.Generator, transition_probability: float
	):
		if transition_probability > 1 or transition_probability < 0:
			raise ValueError(
				f"Transition probabliity must be between 0 and 1, got {transition_probability} instead"
			)
		self.transition_probability = transition_probability

		self.rng: numpy.random.Generator
		if rng_to_use is None:
			self.rng = numpy.random.default_rng()
		else:
			self.rng = rng_to_use

		self.state = 0

	def transition(self) -> float:
		if self.rng.random() < self.transition_probability:
			self.state = 1 - self.state
		return self.state
