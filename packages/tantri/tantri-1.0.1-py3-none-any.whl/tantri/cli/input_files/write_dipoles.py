import numpy
import json


class NumpyEncoder(json.JSONEncoder):
	"""
	Stolen from https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
	"""

	def default(self, obj):
		if isinstance(obj, numpy.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)
