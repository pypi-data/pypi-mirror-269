import pdme.model
import pdme.measurement
import pdme.measurement.input_types
import pdme.subspace_simulation
from typing import Tuple, Dict, NewType, Any
from dataclasses import dataclass
import logging
import numpy
import numpy.random
import pdme.util.fast_v_calc

_logger = logging.getLogger(__name__)


@dataclass
class DirectMonteCarloResult:
	successes: int
	monte_carlo_count: int
	likelihood: float


@dataclass
class DirectMonteCarloConfig:
	monte_carlo_count_per_cycle: int = 10000
	monte_carlo_cycles: int = 10
	target_success: int = 100
	max_monte_carlo_cycles_steps: int = 10
	monte_carlo_seed: int = 1234
	write_successes_to_file: bool = False
	tag: str = ""


# Aliasing dict as a generic data container
DirectMonteCarloData = NewType("DirectMonteCarloData", Dict[str, Any])


class DirectMonteCarloFilter:
	"""
	Abstract class for filtering out samples matching some criteria. Initialise with data as needed,
	then filter out samples as needed.
	"""

	def filter_samples(self, samples: numpy.ndarray) -> numpy.ndarray:
		raise NotImplementedError


class DirectMonteCarloRun:
	"""
	A single model Direct Monte Carlo run, currently implemented only using single threading.
	An encapsulation of the steps needed for a Bayes run.

	Parameters
	----------
	model_name_pair : Sequence[Tuple(str, pdme.model.DipoleModel)]
	The model to evaluate, with name.

	measurements: Sequence[pdme.measurement.DotRangeMeasurement]
	The measurements as dot ranges to use as the bounds for the Monte Carlo calculation.

	monte_carlo_count_per_cycle: int
	The number of Monte Carlo iterations to use in a single cycle calculation.

	monte_carlo_cycles: int
	The number of cycles to use in each step.
	Increasing monte_carlo_count_per_cycle increases memory usage (and runtime), while this increases runtime, allowing
	control over memory use.

	target_success: int
	The number of successes to target before exiting early.
	Should likely be ~100 but can go higher to.

	max_monte_carlo_cycles_steps: int
	The number of steps to use. Each step consists of monte_carlo_cycles cycles, each of which has monte_carlo_count_per_cycle iterations.

	monte_carlo_seed: int
	The seed to use for the RNG.
	"""

	def __init__(
		self,
		model_name_pair: Tuple[str, pdme.model.DipoleModel],
		filter: DirectMonteCarloFilter,
		config: DirectMonteCarloConfig,
	):
		self.model_name, self.model = model_name_pair

		# self.measurements = measurements
		# self.dot_inputs = [(measure.r, measure.f) for measure in self.measurements]

		# self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
		# 	self.dot_inputs
		# )

		self.config = config
		self.filter = filter
		# (
		# 	self.lows,
		# 	self.highs,
		# ) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
		# 	self.measurements
		# )

	def _single_run(self, seed) -> numpy.ndarray:
		rng = numpy.random.default_rng(seed)

		sample_dipoles = self.model.get_monte_carlo_dipole_inputs(
			self.config.monte_carlo_count_per_cycle, -1, rng
		)

		current_sample = sample_dipoles

		return self.filter.filter_samples(current_sample)
		# for di, low, high in zip(self.dot_inputs_array, self.lows, self.highs):

		# 	if len(current_sample) < 1:
		# 		break
		# 	vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
		# 		numpy.array([di]), current_sample
		# 	)

		# 	current_sample = current_sample[
		# 		numpy.all((vals > low) & (vals < high), axis=1)
		# 	]
		# return current_sample

	def execute(self) -> DirectMonteCarloResult:
		step_count = 0
		total_success = 0
		total_count = 0

		count_per_step = (
			self.config.monte_carlo_count_per_cycle * self.config.monte_carlo_cycles
		)
		seed_sequence = numpy.random.SeedSequence(self.config.monte_carlo_seed)
		while (step_count < self.config.max_monte_carlo_cycles_steps) and (
			total_success < self.config.target_success
		):
			_logger.debug(f"Executing step {step_count}")
			for cycle_i, seed in enumerate(
				seed_sequence.spawn(self.config.monte_carlo_cycles)
			):
				cycle_success_configs = self._single_run(seed)
				cycle_success_count = len(cycle_success_configs)
				if cycle_success_count > 0:
					_logger.debug(
						f"For cycle {cycle_i} received {cycle_success_count} successes"
					)
					_logger.debug(cycle_success_configs)
					if self.config.write_successes_to_file:
						sorted_by_freq = numpy.array(
							[
								pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(
									dipole_config
								)
								for dipole_config in cycle_success_configs
							]
						)
						dipole_count = numpy.array(cycle_success_configs).shape[1]
						for n in range(dipole_count):
							numpy.savetxt(
								f"{self.config.tag}_{step_count}_{cycle_i}_dipole_{n}.csv",
								sorted_by_freq[:, n],
								delimiter=",",
							)
				total_success += cycle_success_count
			_logger.debug(f"At end of step {step_count} have {total_success} successes")
			step_count += 1
			total_count += count_per_step

		return DirectMonteCarloResult(
			successes=total_success,
			monte_carlo_count=total_count,
			likelihood=total_success / total_count,
		)
