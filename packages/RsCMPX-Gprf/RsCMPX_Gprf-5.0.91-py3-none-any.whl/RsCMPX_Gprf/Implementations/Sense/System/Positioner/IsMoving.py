from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsMovingCls:
	"""IsMoving commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("isMoving", core, parent)

	def get(self, positioner=repcap.Positioner.Default) -> bool:
		"""SCPI: SENSe:SYSTem:POSitioner<PositionerIdx>:ISMoving \n
		Snippet: value: bool = driver.sense.system.positioner.isMoving.get(positioner = repcap.Positioner.Default) \n
		No command help available \n
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
			:return: is_moving: No help available"""
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		response = self._core.io.query_str(f'SENSe:SYSTem:POSitioner{positioner_cmd_val}:ISMoving?')
		return Conversions.str_to_bool(response)
