import pathlib
import json
import logging
import tantri.cli.input_files
from typing import Sequence
import tantri.dipoles

_logger = logging.getLogger(__name__)

# note that json is insecure by default right?
# but don't worry for now
# TODO: if this ever matters, can improve file handling.


def read_data_from_filename(filename: pathlib.Path):
	try:
		with open(filename, "r") as file:
			return json.load(file)
	except Exception as e:
		_logger.error(
			f"failed to read the file {filename}, raising and aborting", exc_info=e
		)


def read_dots_json_file(filename: pathlib.Path) -> Sequence[tantri.dipoles.DotPosition]:
	data = read_data_from_filename(filename)
	return tantri.cli.input_files.rows_to_dots(data)


def read_dipoles_json_file(filename: pathlib.Path) -> Sequence[tantri.dipoles.DipoleTO]:
	data = read_data_from_filename(filename)
	return tantri.cli.input_files.rows_to_dipoles(data)
