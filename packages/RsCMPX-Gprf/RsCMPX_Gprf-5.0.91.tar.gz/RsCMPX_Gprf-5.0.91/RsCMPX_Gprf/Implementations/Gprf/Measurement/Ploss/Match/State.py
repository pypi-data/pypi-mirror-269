from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	def fetch(self, connection_name: str) -> enums.PathLossState:
		"""SCPI: FETCh:GPRF:MEASurement<instance>:PLOSs:MATCh:STATe \n
		Snippet: value: enums.PathLossState = driver.gprf.measurement.ploss.match.state.fetch(connection_name = 'abc') \n
		No command help available \n
		Suppressed linked return values: reliability \n
			:param connection_name: No help available
			:return: result_state: No help available"""
		param = Conversions.value_to_quoted_str(connection_name)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:GPRF:MEASurement<Instance>:PLOSs:MATCh:STATe? {param}', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.PathLossState)
