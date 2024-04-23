import tantri.dipoles
import numpy
from typing import Sequence


def row_to_dot(input_dict: dict) -> tantri.dipoles.DotPosition:
	r = input_dict["r"]
	if len(r) != 3:
		raise ValueError(
			f"r parameter in input_dict [{input_dict}] does not have length 3"
		)
	label = input_dict["label"]

	return tantri.dipoles.DotPosition(numpy.array(r), label)


def rows_to_dots(
	dot_dict_array: Sequence[dict],
) -> Sequence[tantri.dipoles.DotPosition]:
	return [row_to_dot(input_dict) for input_dict in dot_dict_array]
