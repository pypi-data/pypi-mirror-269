from typing import Sequence
from tantri.dipoles import DipoleTO


def row_to_dipole(input_dict: dict) -> DipoleTO:
	p = input_dict["p"]
	if len(p) != 3:
		raise ValueError(
			f"p parameter in input_dict [{input_dict}] does not have length 3"
		)
	s = input_dict["s"]
	if len(s) != 3:
		raise ValueError(
			f"s parameter in input_dict [{input_dict}] does not have length 3"
		)
	w = input_dict["w"]

	return DipoleTO(p, s, w)


def rows_to_dipoles(dot_dict_array: Sequence[dict]) -> Sequence[DipoleTO]:
	return [row_to_dipole(input_dict) for input_dict in dot_dict_array]
