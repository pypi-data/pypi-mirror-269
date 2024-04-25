from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositionerCls:
	"""Positioner commands group definition. 2 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: Positioner, default value after init: Positioner.Ix1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("positioner", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_positioner_get', 'repcap_positioner_set', repcap.Positioner.Ix1)

	def repcap_positioner_set(self, positioner: repcap.Positioner) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Positioner.Default
		Default value after init: Positioner.Ix1"""
		self._cmd_group.set_repcap_enum_value(positioner)

	def repcap_positioner_get(self) -> repcap.Positioner:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def position(self):
		"""position commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_position'):
			from .Position import PositionCls
			self._position = PositionCls(self._core, self._cmd_group)
		return self._position

	@property
	def isMoving(self):
		"""isMoving commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isMoving'):
			from .IsMoving import IsMovingCls
			self._isMoving = IsMovingCls(self._core, self._cmd_group)
		return self._isMoving

	def clone(self) -> 'PositionerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PositionerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
