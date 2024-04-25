from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PlossCls:
	"""Ploss commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ploss", core, parent)

	def get_cname(self) -> str:
		"""SCPI: CATalog:GPRF:MEASurement<instance>:PLOSs:CNAMe \n
		Snippet: value: str = driver.catalog.gprf.measurement.ploss.get_cname() \n
		Returns the names of the available RF connections. \n
			:return: connection_names: Comma-separated list of strings, one string per RF connection
		"""
		response = self._core.io.query_str('CATalog:GPRF:MEASurement<Instance>:PLOSs:CNAMe?')
		return trim_str_response(response)
