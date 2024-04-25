from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CidxCls:
	"""Cidx commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cidx", core, parent)

	def set(self, row_number: int, connection_index: int) -> None:
		"""SCPI: [CONFigure]:GPRF:MEASurement<instance>:POWer:LIST:CIDX \n
		Snippet: driver.configure.gprf.measurement.power.listPy.cidx.set(row_number = 1, connection_index = 1) \n
		Selects the RF connection index for segment <RowNumber>. For the definition of the connection indices,
		see [CONFigure:]GPRF:MEAS<i>:POWer:LIST:IDX<idx>:CONNection. \n
			:param row_number: No help available
			:param connection_index: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('row_number', row_number, DataType.Integer), ArgSingle('connection_index', connection_index, DataType.Integer))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:LIST:CIDX {param}'.rstrip())

	# noinspection PyTypeChecker
	class CidxStruct(StructBase):
		"""Response structure. Fields: \n
			- Row_Number: int: No parameter help available
			- Connection_Index: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Row_Number'),
			ArgStruct.scalar_int('Connection_Index')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Row_Number: int = None
			self.Connection_Index: int = None

	def get(self) -> CidxStruct:
		"""SCPI: [CONFigure]:GPRF:MEASurement<instance>:POWer:LIST:CIDX \n
		Snippet: value: CidxStruct = driver.configure.gprf.measurement.power.listPy.cidx.get() \n
		Selects the RF connection index for segment <RowNumber>. For the definition of the connection indices,
		see [CONFigure:]GPRF:MEAS<i>:POWer:LIST:IDX<idx>:CONNection. \n
			:return: structure: for return value, see the help for CidxStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:POWer:LIST:CIDX?', self.__class__.CidxStruct())
