from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectionCls:
	"""Connection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	def set(self, connection: str, index=repcap.Index.Default) -> None:
		"""SCPI: [CONFigure]:GPRF:MEASurement<instance>:POWer:LIST:IDX<idx>:CONNection \n
		Snippet: driver.configure.gprf.measurement.power.listPy.idx.connection.set(connection = 'abc', index = repcap.Index.Default) \n
		Assigns a connection to the connection index <idx>. Alternatively, use method RsCMPX_Gprf.Route.Gprf.Measurement.Spath.
		value. For possible <Connection> strings, see [CONFigure:]GPRF:MEAS<i>:POWer:LIST:IDX<idx>:CATalog:CONNection?. \n
			:param connection: No help available
			:param index: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Idx')
		"""
		param = Conversions.value_to_quoted_str(connection)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:LIST:IDX{index_cmd_val}:CONNection {param}')

	def get(self, index=repcap.Index.Default) -> str:
		"""SCPI: [CONFigure]:GPRF:MEASurement<instance>:POWer:LIST:IDX<idx>:CONNection \n
		Snippet: value: str = driver.configure.gprf.measurement.power.listPy.idx.connection.get(index = repcap.Index.Default) \n
		Assigns a connection to the connection index <idx>. Alternatively, use method RsCMPX_Gprf.Route.Gprf.Measurement.Spath.
		value. For possible <Connection> strings, see [CONFigure:]GPRF:MEAS<i>:POWer:LIST:IDX<idx>:CATalog:CONNection?. \n
			:param index: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Idx')
			:return: connection: No help available"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:POWer:LIST:IDX{index_cmd_val}:CONNection?')
		return trim_str_response(response)
