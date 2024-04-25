from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def fetch(self, connection_name: str) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<instance>:PLOSs:EVALuate:FREQuency \n
		Snippet: value: List[float] = driver.gprf.measurement.ploss.evaluate.frequency.fetch(connection_name = 'abc') \n
		Returns the frequency values of the result table for a selected RF connection. The order of the list entries is the same
		as in the command method RsCMPX_Gprf.Gprf.Measurement.Ploss.Evaluate.Gain.fetch. Use this command to check at which
		frequencies the gain values have been measured. For possible connection names, see method RsCMPX_Gprf.Catalog.Gprf.
		Measurement.Ploss.cname. \n
		Suppressed linked return values: reliability \n
			:param connection_name: RF connection for which results are queried.
			:return: frequency: Comma-separated list of frequency values."""
		param = Conversions.value_to_quoted_str(connection_name)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:PLOSs:EVALuate:FREQuency? {param}', suppressed)
		return response
