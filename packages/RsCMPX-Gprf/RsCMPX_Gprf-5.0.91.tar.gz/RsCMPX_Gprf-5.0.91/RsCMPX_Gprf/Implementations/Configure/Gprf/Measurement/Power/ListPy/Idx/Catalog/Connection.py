from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectionCls:
	"""Connection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	def get(self, index=repcap.Index.Default) -> List[str]:
		"""SCPI: [CONFigure]:GPRF:MEASurement<instance>:POWer:LIST:IDX<idx>:CATalog:CONNection \n
		Snippet: value: List[str] = driver.configure.gprf.measurement.power.listPy.idx.catalog.connection.get(index = repcap.Index.Default) \n
		Returns the names of the available connections. \n
			:param index: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Idx')
			:return: connection_source: Comma-separated list of strings, one string per connection"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:POWer:LIST:IDX{index_cmd_val}:CATalog:CONNection?')
		return Conversions.str_to_str_list(response)
