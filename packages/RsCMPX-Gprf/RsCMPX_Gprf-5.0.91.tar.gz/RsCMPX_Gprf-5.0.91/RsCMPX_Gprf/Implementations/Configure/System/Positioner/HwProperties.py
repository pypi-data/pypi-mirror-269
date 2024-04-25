from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HwPropertiesCls:
	"""HwProperties commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hwProperties", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Key: str: No parameter help available
			- Value: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Key'),
			ArgStruct.scalar_str('Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Key: str = None
			self.Value: str = None

	def get(self, positioner=repcap.Positioner.Default) -> GetStruct:
		"""SCPI: [CONFigure]:SYSTem:POSitioner<PositionerIdx>:HWPRoperties \n
		Snippet: value: GetStruct = driver.configure.system.positioner.hwProperties.get(positioner = repcap.Positioner.Default) \n
		No command help available \n
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		return self._core.io.query_struct(f'CONFigure:SYSTem:POSitioner{positioner_cmd_val}:HWPRoperties?', self.__class__.GetStruct())
