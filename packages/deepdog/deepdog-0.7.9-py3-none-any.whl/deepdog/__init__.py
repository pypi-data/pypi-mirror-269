import logging
from deepdog.meta import __version__
from deepdog.bayes_run import BayesRun
from deepdog.bayes_run_simulpairs import BayesRunSimulPairs
from deepdog.real_spectrum_run import RealSpectrumRun
from deepdog.temp_aware_real_spectrum_run import TempAwareRealSpectrumRun
from deepdog.bayes_run_with_ss import BayesRunWithSubspaceSimulation


def get_version():
	return __version__


__all__ = [
	"get_version",
	"BayesRun",
	"BayesRunSimulPairs",
	"RealSpectrumRun",
	"TempAwareRealSpectrumRun",
	"BayesRunWithSubspaceSimulation",
]


logging.getLogger(__name__).addHandler(logging.NullHandler())
