from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositionCls:
	"""Position commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("position", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Theta: float: No parameter help available
			- Phi: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Theta'),
			ArgStruct.scalar_float('Phi')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Theta: float = None
			self.Phi: float = None

	def get(self, positioner=repcap.Positioner.Default) -> GetStruct:
		"""SCPI: SENSe:SYSTem:POSitioner<PositionerIdx>:POSition \n
		Snippet: value: GetStruct = driver.sense.system.positioner.position.get(positioner = repcap.Positioner.Default) \n
		No command help available \n
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		return self._core.io.query_struct(f'SENSe:SYSTem:POSitioner{positioner_cmd_val}:POSition?', self.__class__.GetStruct())
