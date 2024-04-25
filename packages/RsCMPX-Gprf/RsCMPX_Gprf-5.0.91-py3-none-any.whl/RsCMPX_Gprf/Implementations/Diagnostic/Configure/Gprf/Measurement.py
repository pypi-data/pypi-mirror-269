from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MeasurementCls:
	"""Measurement commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	def get_logging(self) -> bool:
		"""SCPI: DIAGnostic:CONFigure:GPRF:MEASurement:LOGGing \n
		Snippet: value: bool = driver.diagnostic.configure.gprf.measurement.get_logging() \n
		No command help available \n
			:return: logging: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:CONFigure:GPRF:MEASurement:LOGGing?')
		return Conversions.str_to_bool(response)

	def set_logging(self, logging: bool) -> None:
		"""SCPI: DIAGnostic:CONFigure:GPRF:MEASurement:LOGGing \n
		Snippet: driver.diagnostic.configure.gprf.measurement.set_logging(logging = False) \n
		No command help available \n
			:param logging: No help available
		"""
		param = Conversions.bool_to_str(logging)
		self._core.io.write(f'DIAGnostic:CONFigure:GPRF:MEASurement:LOGGing {param}')
