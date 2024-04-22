import logging
import numpy
import pdme.measurement
import pdme.measurement.input_types
import pdme.subspace_simulation
from typing import Sequence, Tuple, Optional

from dataclasses import dataclass

_logger = logging.getLogger(__name__)


@dataclass
class SubsetSimulationResult:
	probs_list: Sequence[Tuple]
	over_target_cost: Optional[float]
	over_target_likelihood: Optional[float]
	under_target_cost: Optional[float]
	under_target_likelihood: Optional[float]
	lowest_likelihood: Optional[float]


class SubsetSimulation:
	def __init__(
		self,
		model_name_pair,
		dot_inputs,
		actual_measurements: Sequence[pdme.measurement.DotMeasurement],
		n_c: int,
		n_s: int,
		m_max: int,
		target_cost: Optional[float] = None,
		level_0_seed: int = 200,
		mcmc_seed: int = 20,
		use_adaptive_steps=True,
		default_phi_step=0.01,
		default_theta_step=0.01,
		default_r_step=0.01,
		default_w_log_step=0.01,
		default_upper_w_log_step=4,
		keep_probs_list=True,
		dump_last_generation_to_file=False,
		initial_cost_chunk_size=100,
	):
		name, model = model_name_pair
		self.model_name = name
		self.model = model
		_logger.info(f"got model {self.model_name}")

		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
			dot_inputs
		)
		# _logger.debug(f"actual measurements: {actual_measurements}")
		self.actual_measurement_array = numpy.array([m.v for m in actual_measurements])

		def cost_function_to_use(dipoles_to_test):
			return pdme.subspace_simulation.proportional_costs_vs_actual_measurement(
				self.dot_inputs_array, self.actual_measurement_array, dipoles_to_test
			)

		self.cost_function_to_use = cost_function_to_use

		self.n_c = n_c
		self.n_s = n_s
		self.m_max = m_max

		self.level_0_seed = level_0_seed
		self.mcmc_seed = mcmc_seed

		self.use_adaptive_steps = use_adaptive_steps
		self.default_phi_step = default_phi_step
		self.default_theta_step = default_theta_step
		self.default_r_step = default_r_step
		self.default_w_log_step = default_w_log_step
		self.default_upper_w_log_step = default_upper_w_log_step

		_logger.info("using params:")
		_logger.info(f"\tn_c: {self.n_c}")
		_logger.info(f"\tn_s: {self.n_s}")
		_logger.info(f"\tm: {self.m_max}")
		_logger.info("let's do level 0...")

		self.target_cost = target_cost
		_logger.info(f"will stop at target cost {target_cost}")

		self.keep_probs_list = keep_probs_list
		self.dump_last_generations = dump_last_generation_to_file

		self.initial_cost_chunk_size = initial_cost_chunk_size

	def execute(self) -> SubsetSimulationResult:

		probs_list = []

		sample_dipoles = self.model.get_monte_carlo_dipole_inputs(
			self.n_c * self.n_s,
			-1,
			rng_to_use=numpy.random.default_rng(self.level_0_seed),
		)
		# _logger.debug(sample_dipoles)
		# _logger.debug(sample_dipoles.shape)

		raw_costs = []
		_logger.debug(
			f"Using iterated cost function thing with chunk size {self.initial_cost_chunk_size}"
		)

		for x in range(0, len(sample_dipoles), self.initial_cost_chunk_size):
			_logger.debug(f"doing chunk {x}")
			raw_costs.extend(
				self.cost_function_to_use(
					sample_dipoles[x : x + self.initial_cost_chunk_size]
				)
			)
		costs = numpy.array(raw_costs)

		_logger.debug(f"costs: {costs}")
		sorted_indexes = costs.argsort()[::-1]

		_logger.debug(costs[sorted_indexes])
		_logger.debug(sample_dipoles[sorted_indexes])

		sorted_costs = costs[sorted_indexes]
		sorted_dipoles = sample_dipoles[sorted_indexes]

		threshold_cost = sorted_costs[-self.n_c]

		all_dipoles = numpy.array(
			[
				pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(samp)
				for samp in sorted_dipoles
			]
		)
		all_chains = list(zip(sorted_costs, all_dipoles))

		mcmc_rng = numpy.random.default_rng(self.mcmc_seed)

		for i in range(self.m_max):
			next_seeds = all_chains[-self.n_c :]

			if self.dump_last_generations:
				_logger.info("writing out csv file")
				next_dipoles_seed_dipoles = numpy.array([n[1] for n in next_seeds])
				for n in range(self.model.n):
					_logger.info(f"{next_dipoles_seed_dipoles[:, n].shape}")
					numpy.savetxt(
						f"generation_{self.n_c}_{self.n_s}_{i}_dipole_{n}.csv",
						next_dipoles_seed_dipoles[:, n],
						delimiter=",",
					)

				next_seeds_as_array = numpy.array([s for _, s in next_seeds])
				stdevs = self.get_stdevs_from_arrays(next_seeds_as_array)
				_logger.info(f"got stdevs: {stdevs.stdevs}")
				all_long_chains = []
				for seed_index, (c, s) in enumerate(
					next_seeds[:: len(next_seeds) // 20]
				):
					# chain = mcmc(s, threshold_cost, n_s, model, dot_inputs_array, actual_measurement_array, mcmc_rng, curr_cost=c, stdevs=stdevs)
					# until new version gotta do
					_logger.debug(f"\t{seed_index}: doing long chain on the next seed")

					long_chain = self.model.get_mcmc_chain(
						s,
						self.cost_function_to_use,
						1000,
						threshold_cost,
						stdevs,
						initial_cost=c,
						rng_arg=mcmc_rng,
					)
					for _, chained in long_chain:
						all_long_chains.append(chained)
				all_long_chains_array = numpy.array(all_long_chains)
				for n in range(self.model.n):
					_logger.info(f"{all_long_chains_array[:, n].shape}")
					numpy.savetxt(
						f"long_chain_generation_{self.n_c}_{self.n_s}_{i}_dipole_{n}.csv",
						all_long_chains_array[:, n],
						delimiter=",",
					)

			if self.keep_probs_list:
				for cost_index, cost_chain in enumerate(all_chains[: -self.n_c]):
					probs_list.append(
						(
							((self.n_c * self.n_s - cost_index) / (self.n_c * self.n_s))
							/ (self.n_s ** (i)),
							cost_chain[0],
							i + 1,
						)
					)

			next_seeds_as_array = numpy.array([s for _, s in next_seeds])

			stdevs = self.get_stdevs_from_arrays(next_seeds_as_array)
			_logger.info(f"got stdevs: {stdevs.stdevs}")
			_logger.debug("Starting the MCMC")
			all_chains = []
			for seed_index, (c, s) in enumerate(next_seeds):
				# chain = mcmc(s, threshold_cost, n_s, model, dot_inputs_array, actual_measurement_array, mcmc_rng, curr_cost=c, stdevs=stdevs)
				# until new version gotta do
				_logger.debug(
					f"\t{seed_index}: getting another chain from the next seed"
				)
				chain = self.model.get_mcmc_chain(
					s,
					self.cost_function_to_use,
					self.n_s,
					threshold_cost,
					stdevs,
					initial_cost=c,
					rng_arg=mcmc_rng,
				)
				for cost, chained in chain:
					try:
						filtered_cost = cost[0]
					except (IndexError, TypeError):
						filtered_cost = cost
					all_chains.append((filtered_cost, chained))
			_logger.debug("finished mcmc")
			# _logger.debug(all_chains)

			all_chains.sort(key=lambda c: c[0], reverse=True)
			_logger.debug("finished sorting all_chains")

			threshold_cost = all_chains[-self.n_c][0]
			_logger.info(
				f"current threshold cost: {threshold_cost}, at P = (1 / {self.n_s})^{i + 1}"
			)
			if (self.target_cost is not None) and (threshold_cost < self.target_cost):
				_logger.info(
					f"got a threshold cost {threshold_cost}, less than {self.target_cost}. will leave early"
				)

				cost_list = [c[0] for c in all_chains]
				over_index = reverse_bisect_right(cost_list, self.target_cost)

				shorter_probs_list = []
				for cost_index, cost_chain in enumerate(all_chains):
					if self.keep_probs_list:
						probs_list.append(
							(
								(
									(self.n_c * self.n_s - cost_index)
									/ (self.n_c * self.n_s)
								)
								/ (self.n_s ** (i)),
								cost_chain[0],
								i + 1,
							)
						)
					shorter_probs_list.append(
						(
							cost_chain[0],
							((self.n_c * self.n_s - cost_index) / (self.n_c * self.n_s))
							/ (self.n_s ** (i)),
						)
					)
				# _logger.info(shorter_probs_list)
				result = SubsetSimulationResult(
					probs_list=probs_list,
					over_target_cost=shorter_probs_list[over_index - 1][0],
					over_target_likelihood=shorter_probs_list[over_index - 1][1],
					under_target_cost=shorter_probs_list[over_index][0],
					under_target_likelihood=shorter_probs_list[over_index][1],
					lowest_likelihood=shorter_probs_list[-1][1],
				)
				return result

			# _logger.debug([c[0] for c in all_chains[-n_c:]])
			_logger.info(f"doing level {i + 1}")

		if self.keep_probs_list:
			for cost_index, cost_chain in enumerate(all_chains):
				probs_list.append(
					(
						((self.n_c * self.n_s - cost_index) / (self.n_c * self.n_s))
						/ (self.n_s ** (self.m_max)),
						cost_chain[0],
						self.m_max + 1,
					)
				)
		threshold_cost = all_chains[-self.n_c][0]
		_logger.info(
			f"final threshold cost: {threshold_cost}, at P = (1 / {self.n_s})^{self.m_max + 1}"
		)
		for a in all_chains[-10:]:
			_logger.info(a)
		# for prob, prob_cost in probs_list:
		# 	_logger.info(f"\t{prob}: {prob_cost}")
		probs_list.sort(key=lambda c: c[0], reverse=True)

		min_likelihood = ((1) / (self.n_c * self.n_s)) / (self.n_s ** (self.m_max))

		result = SubsetSimulationResult(
			probs_list=probs_list,
			over_target_cost=None,
			over_target_likelihood=None,
			under_target_cost=None,
			under_target_likelihood=None,
			lowest_likelihood=min_likelihood,
		)
		return result

	def get_stdevs_from_arrays(
		self, array
	) -> pdme.subspace_simulation.MCMCStandardDeviation:
		# stdevs = get_stdevs_from_arrays(next_seeds_as_array, model)
		if self.use_adaptive_steps:

			stdev_array = []
			count = array.shape[1]
			for dipole_index in range(count):
				selected = array[:, dipole_index]
				pxs = selected[:, 0]
				pys = selected[:, 1]
				pzs = selected[:, 2]
				thetas = numpy.arccos(pzs / self.model.pfixed)
				phis = numpy.arctan2(pys, pxs)

				rstdevs = numpy.maximum(
					numpy.std(selected, axis=0)[3:6],
					self.default_r_step / (self.n_s * 10),
				)
				frequency_stdevs = numpy.minimum(
					numpy.maximum(
						numpy.std(numpy.log(selected[:, -1])),
						self.default_w_log_step / (self.n_s * 10),
					),
					self.default_upper_w_log_step,
				)
				stdev_array.append(
					pdme.subspace_simulation.DipoleStandardDeviation(
						p_theta_step=max(
							numpy.std(thetas), self.default_theta_step / (self.n_s * 10)
						),
						p_phi_step=max(
							numpy.std(phis), self.default_phi_step / (self.n_s * 10)
						),
						rx_step=rstdevs[0],
						ry_step=rstdevs[1],
						rz_step=rstdevs[2],
						w_log_step=frequency_stdevs,
					)
				)
		else:
			default_stdev = pdme.subspace_simulation.DipoleStandardDeviation(
				self.default_phi_step,
				self.default_theta_step,
				self.default_r_step,
				self.default_r_step,
				self.default_r_step,
				self.default_w_log_step,
			)
			stdev_array = [default_stdev]
		stdevs = pdme.subspace_simulation.MCMCStandardDeviation(stdev_array)
		return stdevs


def reverse_bisect_right(a, x, lo=0, hi=None):
	"""Return the index where to insert item x in list a, assuming a is sorted in descending order.

	The return value i is such that all e in a[:i] have e >= x, and all e in
	a[i:] have e < x.  So if x already appears in the list, a.insert(x) will
	insert just after the rightmost x already there.

	Optional args lo (default 0) and hi (default len(a)) bound the
	slice of a to be searched.

	Essentially, the function returns number of elements in a which are >= than x.
	>>> a = [8, 6, 5, 4, 2]
	>>> reverse_bisect_right(a, 5)
	3
	>>> a[:reverse_bisect_right(a, 5)]
	[8, 6, 5]
	"""
	if lo < 0:
		raise ValueError("lo must be non-negative")
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo + hi) // 2
		if x > a[mid]:
			hi = mid
		else:
			lo = mid + 1
	return lo
