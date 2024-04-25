from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToCls:
	"""To commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("to", core, parent)

	def set(self, theta: float, phi: float, positioner=repcap.Positioner.Default) -> None:
		"""SCPI: [CONFigure]:SYSTem:POSitioner<PositionerIdx>:MOVE:TO \n
		Snippet: driver.configure.system.positioner.move.to.set(theta = 1.0, phi = 1.0, positioner = repcap.Positioner.Default) \n
		No command help available \n
			:param theta: No help available
			:param phi: No help available
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('theta', theta, DataType.Float), ArgSingle('phi', phi, DataType.Float))
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		self._core.io.write(f'CONFigure:SYSTem:POSitioner{positioner_cmd_val}:MOVE:TO {param}'.rstrip())
