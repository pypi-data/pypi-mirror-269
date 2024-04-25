from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositionerCls:
	"""Positioner commands group definition. 4 total commands, 4 Subgroups, 0 group commands
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
	def hwProperties(self):
		"""hwProperties commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hwProperties'):
			from .HwProperties import HwPropertiesCls
			self._hwProperties = HwPropertiesCls(self._core, self._cmd_group)
		return self._hwProperties

	@property
	def versions(self):
		"""versions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_versions'):
			from .Versions import VersionsCls
			self._versions = VersionsCls(self._core, self._cmd_group)
		return self._versions

	@property
	def move(self):
		"""move commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_move'):
			from .Move import MoveCls
			self._move = MoveCls(self._core, self._cmd_group)
		return self._move

	@property
	def moving(self):
		"""moving commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_moving'):
			from .Moving import MovingCls
			self._moving = MovingCls(self._core, self._cmd_group)
		return self._moving

	def clone(self) -> 'PositionerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PositionerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
