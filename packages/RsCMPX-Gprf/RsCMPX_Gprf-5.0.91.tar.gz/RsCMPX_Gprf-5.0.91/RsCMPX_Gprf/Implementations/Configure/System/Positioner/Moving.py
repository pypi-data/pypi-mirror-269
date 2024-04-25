from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MovingCls:
	"""Moving commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("moving", core, parent)

	def stop(self, positioner=repcap.Positioner.Default) -> None:
		"""SCPI: [CONFigure]:SYSTem:POSitioner<PositionerIdx>:MOVing:STOP \n
		Snippet: driver.configure.system.positioner.moving.stop(positioner = repcap.Positioner.Default) \n
		No command help available \n
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
		"""
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		self._core.io.write(f'CONFigure:SYSTem:POSitioner{positioner_cmd_val}:MOVing:STOP')

	def stop_with_opc(self, positioner=repcap.Positioner.Default, opc_timeout_ms: int = -1) -> None:
		positioner_cmd_val = self._cmd_group.get_repcap_cmd_value(positioner, repcap.Positioner)
		"""SCPI: [CONFigure]:SYSTem:POSitioner<PositionerIdx>:MOVing:STOP \n
		Snippet: driver.configure.system.positioner.moving.stop_with_opc(positioner = repcap.Positioner.Default) \n
		No command help available \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCMPX_Gprf.utilities.opc_timeout_set() to set the timeout value. \n
			:param positioner: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Positioner')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:SYSTem:POSitioner{positioner_cmd_val}:MOVing:STOP', opc_timeout_ms)
