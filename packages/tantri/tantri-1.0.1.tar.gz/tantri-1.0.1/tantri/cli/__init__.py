import click
import logging
import tantri
import numpy
import tantri.cli.input_files.write_dipoles
import tantri.cli.file_importer
import tantri.dipoles
import json
import tantri.dipoles.generation
import pathlib
import tqdm  # type: ignore

_logger = logging.getLogger(__name__)

LOG_PATTERN = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


POTENTIAL = "electric-potential"
X_ELECTRIC_FIELD = "x-electric-field"


def _set_up_logging(filename):
	handlers = [logging.StreamHandler()]
	if filename is not None:
		handlers.append(logging.FileHandler(filename))
	logging.basicConfig(
		level=logging.DEBUG,
		format=LOG_PATTERN,
		handlers=handlers,
	)
	logging.getLogger("pdme").setLevel(logging.INFO)
	logging.captureWarnings(True)


@click.group()
@click.option(
	"--log", help="Enable logging to stream only", is_flag=True, default=False
)
@click.option("--log-file", help="A filename to use for logging (implies --log)")
@click.version_option(tantri.get_version())
def cli(log, log_file):
	"""Utilities for generating simulated TLS time series data."""
	if log or (log_file is not None):
		# log file has been provided, let's log
		_set_up_logging(log_file)


@cli.command()
@click.option(
	"--dipoles-file",
	default="dipoles.json",
	show_default=True,
	type=click.Path(exists=True, path_type=pathlib.Path),
	help="File with json array of dipoles",
)
@click.option(
	"--dots-file",
	default="dots.json",
	show_default=True,
	type=click.Path(exists=True, path_type=pathlib.Path),
	help="File with json array of dots",
)
@click.option(
	"--measurement-type",
	type=click.Choice([POTENTIAL, X_ELECTRIC_FIELD]),
	default=POTENTIAL,
	help="The type of measurement to simulate",
	show_default=True,
)
@click.option(
	"--delta-t",
	"-t",
	type=float,
	default=1,
	help="The delta t between time series iterations.",
	show_default=True,
)
@click.option(
	"--num-iterations",
	"-n",
	type=int,
	default=10,
	help="The number of iterations.",
	show_default=True,
)
@click.option(
	"--time-series-rng-seed",
	"-s",
	type=int,
	default=None,
	help="A seed to use to create an override default rng. You should set this.",
)
@click.option(
	"output_file",
	"-o",
	type=click.File("w"),
	help="The output file to write, in csv format",
	required=True,
)
@click.option("--header-row/--no-header-row", default=False, help="Write a header row")
def write_time_series(
	dipoles_file,
	dots_file,
	measurement_type,
	delta_t,
	num_iterations,
	time_series_rng_seed,
	output_file,
	header_row,
):
	"""
	Generate a time series for the passed in parameters.
	"""
	_logger.debug(
		f"Received parameters [dipoles_file: {dipoles_file}] and [dots_file: {dots_file}]"
	)
	dipoles = tantri.cli.file_importer.read_dipoles_json_file(dipoles_file)
	dots = tantri.cli.file_importer.read_dots_json_file(dots_file)

	if measurement_type == POTENTIAL:
		measurement_enum = tantri.dipoles.DipoleMeasurementType.ELECTRIC_POTENTIAL
		value_name = "V"
	elif measurement_type == X_ELECTRIC_FIELD:
		measurement_enum = tantri.dipoles.DipoleMeasurementType.X_ELECTRIC_FIELD
		value_name = "Ex"

	_logger.debug(f"Using measurement {measurement_enum.name}")
	labels = [dot.label for dot in dots]
	if header_row:
		value_labels = ", ".join([f"{value_name}_{label}" for label in labels])
		output_file.write(f"t (s), {value_labels}\n")

	_logger.debug(
		f"Going to simulate {num_iterations} iterations with a delta t of {delta_t}"
	)

	_logger.debug(f"Got seed {time_series_rng_seed}")
	if time_series_rng_seed is None:
		time_series = tantri.dipoles.DipoleTimeSeries(
			dipoles, dots, measurement_enum, delta_t
		)
	else:
		rng = numpy.random.default_rng(time_series_rng_seed)
		time_series = tantri.dipoles.DipoleTimeSeries(
			dipoles, dots, measurement_enum, delta_t, rng
		)

	for i in tqdm.trange(num_iterations):
		transition = time_series.transition()
		transition_values = ", ".join(str(transition[label]) for label in labels)
		output_file.write(f"{i * delta_t}, {transition_values}\n")


@cli.command()
@click.argument(
	"generation_config",
	type=click.Path(exists=True, path_type=pathlib.Path),
)
@click.argument(
	"output_file",
	type=click.File("w"),
)
@click.option(
	"--override-rng-seed", type=int, help="Seed to override the generation config spec."
)
def generate_dipoles(generation_config, output_file, override_rng_seed):
	"""Generate random dipoles as described by GENERATION_CONFIG and output to OUTPUT_FILE.

	GENERATION_CONFIG should be a JSON file that matches the appropriate spec, and OUTPUT_FILE will contain JSON formatted contents.
	OUTPUT_FILE will be overwritten, if it exists.

	If the --override-rng-seed is set, it's better to keep logs of the generation!
	"""
	_logger.debug(
		f"generate_dipoles was called, with config file {click.format_filename(generation_config)}"
	)
	_logger.debug(f"override_rng_seed: [{override_rng_seed}]")

	with open(generation_config, "r") as config_file:
		data = json.load(config_file)
	config = tantri.dipoles.generation.DipoleGenerationConfig(**data)

	override_rng = None
	if override_rng_seed is not None:
		_logger.info(f"Overriding the rng with a new one with seed {override_rng_seed}")
		override_rng = numpy.random.default_rng(override_rng_seed)
	_logger.debug(f"generating dipoles with config {config}...")
	generated = tantri.dipoles.generation.make_dipoles(config, override_rng)

	output_file.write(
		json.dumps(
			[g.as_dict() for g in generated],
			cls=tantri.cli.input_files.write_dipoles.NumpyEncoder,
		)
	)
