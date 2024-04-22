from numpy import ndarray
from deepdog.direct_monte_carlo.direct_mc import DirectMonteCarloFilter
from typing import Sequence
import pdme.measurement
import pdme.measurement.input_types
import pdme.util.fast_nonlocal_spectrum
import pdme.util.fast_v_calc
import numpy


class SingleDotPotentialFilter(DirectMonteCarloFilter):
	def __init__(self, measurements: Sequence[pdme.measurement.DotRangeMeasurement]):
		self.measurements = measurements
		self.dot_inputs = [(measure.r, measure.f) for measure in self.measurements]

		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
			self.dot_inputs
		)
		(
			self.lows,
			self.highs,
		) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
			self.measurements
		)

	def filter_samples(self, samples: ndarray) -> ndarray:
		current_sample = samples
		for di, low, high in zip(self.dot_inputs_array, self.lows, self.highs):

			if len(current_sample) < 1:
				break
			vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
				numpy.array([di]), current_sample
			)

			current_sample = current_sample[
				numpy.all((vals > low) & (vals < high), axis=1)
			]
		return current_sample


class DoubleDotSpinQubitFrequencyFilter(DirectMonteCarloFilter):
	def __init__(
		self,
		pair_phase_measurements: Sequence[pdme.measurement.DotPairRangeMeasurement],
	):
		self.pair_phase_measurements = pair_phase_measurements
		self.dot_pair_inputs = [
			(measure.r1, measure.r2, measure.f)
			for measure in self.pair_phase_measurements
		]
		self.dot_pair_inputs_array = (
			pdme.measurement.input_types.dot_pair_inputs_to_array(self.dot_pair_inputs)
		)
		(
			self.pair_phase_lows,
			self.pair_phase_highs,
		) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
			self.pair_phase_measurements
		)

	def fast_s_spin_qubit_tarucha_nonlocal_dipoleses(
		self, dot_pair_inputs: numpy.ndarray, dipoleses: numpy.ndarray
	) -> numpy.ndarray:
		"""
		No error correction here baby.
		"""
		ps = dipoleses[:, :, 0:3]
		ss = dipoleses[:, :, 3:6]
		ws = dipoleses[:, :, 6]

		r1s = dot_pair_inputs[:, 0, 0:3]
		r2s = dot_pair_inputs[:, 1, 0:3]
		f1s = dot_pair_inputs[:, 0, 3]
		# Don't actually need this
		# f2s = dot_pair_inputs[:, 1, 3]

		diffses1 = r1s[:, None] - ss[:, None, :]
		diffses2 = r2s[:, None] - ss[:, None, :]

		norms1 = numpy.linalg.norm(diffses1, axis=3)
		norms2 = numpy.linalg.norm(diffses2, axis=3)

		alphses1 = (
			(
				3
				* numpy.transpose(
					numpy.transpose(
						numpy.einsum("abcd,acd->abc", diffses1, ps) / (norms1**2)
					)
					* numpy.transpose(diffses1)
				)[:, :, :, 0]
			)
			- ps[:, :, 0, numpy.newaxis]
		) / (norms1**3)
		alphses2 = (
			(
				3
				* numpy.transpose(
					numpy.transpose(
						numpy.einsum("abcd,acd->abc", diffses2, ps) / (norms2**2)
					)
					* numpy.transpose(diffses2)
				)[:, :, :, 0]
			)
			- ps[:, :, 0, numpy.newaxis]
		) / (norms2**3)

		bses = (1 / numpy.pi) * (
			ws[:, None, :] / (f1s[:, None] ** 2 + ws[:, None, :] ** 2)
		)

		return numpy.einsum("...j->...", alphses1 * alphses2 * bses)

	def filter_samples(self, samples: ndarray) -> ndarray:
		current_sample = samples

		for pi, plow, phigh in zip(
			self.dot_pair_inputs_array, self.pair_phase_lows, self.pair_phase_highs
		):
			if len(current_sample) < 1:
				break

			###
			# This should be  abstracted out, but we're going to dump it here for time pressure's sake
			###
			# vals = pdme.util.fast_nonlocal_spectrum.signarg(
			# 	pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(
			# 		numpy.array([pi]), current_sample
			# 	)
			#
			vals = pdme.util.fast_nonlocal_spectrum.signarg(
				self.fast_s_spin_qubit_tarucha_nonlocal_dipoleses(
					numpy.array([pi]), current_sample
				)
			)
			current_sample = current_sample[
				numpy.all(
					((vals > plow) & (vals < phigh)) | ((vals < plow) & (vals > phigh)),
					axis=1,
				)
			]
		return current_sample
