from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, connection_name: str, num_entries: int, frequency: List[float]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<instance>:PLOSs:LIST:FREQuency \n
		Snippet: driver.configure.gprf.measurement.ploss.listPy.frequency.set(connection_name = 'abc', num_entries = 1, frequency = [1.1, 2.2, 3.3]) \n
		Configures the frequency list for a selected RF connection. For possible connection names, see method RsCMPX_Gprf.Catalog.
		Gprf.Measurement.Ploss.cname. For the supported frequency range, see 'Frequency ranges'. \n
			:param connection_name: RF connection for which the frequency list is configured.
			:param num_entries: Configures the number of frequencies to be defined.
			:param frequency: Comma-separated list of NumEntries frequencies.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('connection_name', connection_name, DataType.String), ArgSingle('num_entries', num_entries, DataType.Integer), ArgSingle.as_open_list('frequency', frequency, DataType.FloatList, None))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:PLOSs:LIST:FREQuency {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Num_Entries: int: Configures the number of frequencies to be defined.
			- Frequency: List[float]: Comma-separated list of NumEntries frequencies."""
		__meta_args_list = [
			ArgStruct.scalar_int('Num_Entries'),
			ArgStruct('Frequency', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Num_Entries: int = None
			self.Frequency: List[float] = None

	def get(self, connection_name: str) -> GetStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<instance>:PLOSs:LIST:FREQuency \n
		Snippet: value: GetStruct = driver.configure.gprf.measurement.ploss.listPy.frequency.get(connection_name = 'abc') \n
		Configures the frequency list for a selected RF connection. For possible connection names, see method RsCMPX_Gprf.Catalog.
		Gprf.Measurement.Ploss.cname. For the supported frequency range, see 'Frequency ranges'. \n
			:param connection_name: RF connection for which the frequency list is configured.
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.value_to_quoted_str(connection_name)
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:PLOSs:LIST:FREQuency? {param}', self.__class__.GetStruct())
