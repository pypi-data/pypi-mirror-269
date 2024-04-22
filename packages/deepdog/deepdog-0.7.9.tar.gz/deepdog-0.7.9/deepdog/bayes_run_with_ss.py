import deepdog.subset_simulation
import pdme.inputs
import pdme.model
import pdme.measurement.input_types
import pdme.measurement.oscillating_dipole
import pdme.util.fast_v_calc
import pdme.util.fast_nonlocal_spectrum
from typing import Sequence, Tuple, List, Optional
import datetime
import csv
import logging
import numpy
import numpy.typing


# TODO: remove hardcode
CHUNKSIZE = 50

# TODO: It's garbage to have this here duplicated from pdme.
DotInput = Tuple[numpy.typing.ArrayLike, float]


CLAMPING_FACTOR = 10

_logger = logging.getLogger(__name__)


class BayesRunWithSubspaceSimulation:
	"""
	A single Bayes run for a given set of dots.

	Parameters
	----------
	dot_inputs : Sequence[DotInput]
	The dot inputs for this bayes run.

	models_with_names : Sequence[Tuple(str, pdme.model.DipoleModel)]
	The models to evaluate.

	actual_model : pdme.model.DipoleModel
	The model which is actually correct.

	filename_slug : str
	The filename slug to include.

	run_count: int
	The number of runs to do.
	"""

	def __init__(
		self,
		dot_positions: Sequence[numpy.typing.ArrayLike],
		frequency_range: Sequence[float],
		models_with_names: Sequence[Tuple[str, pdme.model.DipoleModel]],
		actual_model: pdme.model.DipoleModel,
		filename_slug: str,
		max_frequency: float = 20,
		end_threshold: float = None,
		run_count=100,
		chunksize: int = CHUNKSIZE,
		ss_n_c: int = 500,
		ss_n_s: int = 100,
		ss_m_max: int = 15,
		ss_target_cost: Optional[float] = None,
		ss_level_0_seed: int = 200,
		ss_mcmc_seed: int = 20,
		ss_use_adaptive_steps=True,
		ss_default_phi_step=0.01,
		ss_default_theta_step=0.01,
		ss_default_r_step=0.01,
		ss_default_w_log_step=0.01,
		ss_default_upper_w_log_step=4,
		ss_dump_last_generation=False,
		ss_initial_costs_chunk_size=100,
		write_output_to_bayesruncsv=True,
		use_timestamp_for_output=True,
	) -> None:
		self.dot_inputs = pdme.inputs.inputs_with_frequency_range(
			dot_positions, frequency_range
		)
		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
			self.dot_inputs
		)

		self.models_with_names = models_with_names
		self.models = [model for (_, model) in models_with_names]
		self.model_names = [name for (name, _) in models_with_names]
		self.actual_model = actual_model

		self.n: int
		try:
			self.n = self.actual_model.n  # type: ignore
		except AttributeError:
			self.n = 1

		self.model_count = len(self.models)

		self.csv_fields = []
		for i in range(self.n):
			self.csv_fields.extend(
				[
					f"dipole_moment_{i+1}",
					f"dipole_location_{i+1}",
					f"dipole_frequency_{i+1}",
				]
			)
		self.compensate_zeros = True
		self.chunksize = chunksize
		for name in self.model_names:
			self.csv_fields.extend([f"{name}_likelihood", f"{name}_prob"])

		self.probabilities = [1 / self.model_count] * self.model_count

		if use_timestamp_for_output:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
			self.filename = f"{timestamp}-{filename_slug}.bayesrunwithss.csv"
		else:
			self.filename = f"{filename_slug}.bayesrunwithss.csv"
		self.max_frequency = max_frequency

		if end_threshold is not None:
			if 0 < end_threshold < 1:
				self.end_threshold: float = end_threshold
				self.use_end_threshold = True
				_logger.info(f"Will abort early, at {self.end_threshold}.")
			else:
				raise ValueError(
					f"end_threshold should be between 0 and 1, but is actually {end_threshold}"
				)

		self.ss_n_c = ss_n_c
		self.ss_n_s = ss_n_s
		self.ss_m_max = ss_m_max
		self.ss_target_cost = ss_target_cost
		self.ss_level_0_seed = ss_level_0_seed
		self.ss_mcmc_seed = ss_mcmc_seed
		self.ss_use_adaptive_steps = ss_use_adaptive_steps
		self.ss_default_phi_step = ss_default_phi_step
		self.ss_default_theta_step = ss_default_theta_step
		self.ss_default_r_step = ss_default_r_step
		self.ss_default_w_log_step = ss_default_w_log_step
		self.ss_default_upper_w_log_step = ss_default_upper_w_log_step
		self.ss_dump_last_generation = ss_dump_last_generation
		self.ss_initial_costs_chunk_size = ss_initial_costs_chunk_size
		self.run_count = run_count

		self.write_output_to_csv = write_output_to_bayesruncsv

	def go(self) -> Sequence:

		if self.write_output_to_csv:
			with open(self.filename, "a", newline="") as outfile:
				writer = csv.DictWriter(
					outfile, fieldnames=self.csv_fields, dialect="unix"
				)
				writer.writeheader()

		return_result = []

		for run in range(1, self.run_count + 1):

			# Generate the actual dipoles
			actual_dipoles = self.actual_model.get_dipoles(self.max_frequency)

			measurements = actual_dipoles.get_dot_measurements(self.dot_inputs)

			_logger.info(f"Going to work on dipole at {actual_dipoles.dipoles}")

			# define a new seed sequence for each run

			results = []
			_logger.debug("Going to iterate over models now")
			for model_count, model in enumerate(self.models_with_names):
				_logger.debug(f"Doing model #{model_count}, {model[0]}")
				subset_run = deepdog.subset_simulation.SubsetSimulation(
					model,
					self.dot_inputs,
					measurements,
					self.ss_n_c,
					self.ss_n_s,
					self.ss_m_max,
					self.ss_target_cost,
					self.ss_level_0_seed,
					self.ss_mcmc_seed,
					self.ss_use_adaptive_steps,
					self.ss_default_phi_step,
					self.ss_default_theta_step,
					self.ss_default_r_step,
					self.ss_default_w_log_step,
					self.ss_default_upper_w_log_step,
					initial_cost_chunk_size=self.ss_initial_costs_chunk_size,
					keep_probs_list=False,
					dump_last_generation_to_file=self.ss_dump_last_generation,
				)
				results.append(subset_run.execute())

			_logger.debug("Done, constructing output now")
			row = {
				"dipole_moment_1": actual_dipoles.dipoles[0].p,
				"dipole_location_1": actual_dipoles.dipoles[0].s,
				"dipole_frequency_1": actual_dipoles.dipoles[0].w,
			}
			for i in range(1, self.n):
				try:
					current_dipoles = actual_dipoles.dipoles[i]
					row[f"dipole_moment_{i+1}"] = current_dipoles.p
					row[f"dipole_location_{i+1}"] = current_dipoles.s
					row[f"dipole_frequency_{i+1}"] = current_dipoles.w
				except IndexError:
					_logger.info(f"Not writing anymore, saw end after {i}")
					break

			likelihoods: List[float] = []

			for (name, result) in zip(self.model_names, results):
				if result.over_target_likelihood is None:
					if result.lowest_likelihood is None:
						_logger.error(f"result {result} looks bad")
						clamped_likelihood = 10**-15
					else:
						clamped_likelihood = result.lowest_likelihood / CLAMPING_FACTOR
					_logger.warning(
						f"got a none result, clamping to {clamped_likelihood}"
					)
				else:
					clamped_likelihood = result.over_target_likelihood
				likelihoods.append(clamped_likelihood)
				row[f"{name}_likelihood"] = clamped_likelihood

			success_weight = sum(
				[
					likelihood * prob
					for likelihood, prob in zip(likelihoods, self.probabilities)
				]
			)
			new_probabilities = [
				likelihood * old_prob / success_weight
				for likelihood, old_prob in zip(likelihoods, self.probabilities)
			]
			self.probabilities = new_probabilities
			for name, probability in zip(self.model_names, self.probabilities):
				row[f"{name}_prob"] = probability
			_logger.info(row)
			return_result.append(row)

			if self.write_output_to_csv:
				with open(self.filename, "a", newline="") as outfile:
					writer = csv.DictWriter(
						outfile, fieldnames=self.csv_fields, dialect="unix"
					)
					writer.writerow(row)

			if self.use_end_threshold:
				max_prob = max(self.probabilities)
				if max_prob > self.end_threshold:
					_logger.info(
						f"Aborting early, because {max_prob} is greater than {self.end_threshold}"
					)
					break

		return return_result
