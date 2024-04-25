from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VersionsCls:
	"""Versions commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("versions", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Firmware_Vers: str: No parameter help available
			- Driver_Vers: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Firmware_Vers'),
			ArgStruct.scalar_str('Driver_Vers')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Firmware_Vers: str = None
			self.Driver_Vers: str = None

	def get(self, positioner=repcap.Positioner.Default) -> GetStruct:
		"""SCPI: [CONFigure]:SYSTem:POSitioner<PositionerIdx>:VERSions \n
		Snippet: value: GetStruct = driver.configure.system.positioner.versions.get(positioner = repcap.Positioner.Default) \n
		No command help available \n
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		return self._core.io.query_struct(f'CONFigure:SYSTem:POSitioner{positioner_cmd_val}:VERSions?', self.__class__.GetStruct())
