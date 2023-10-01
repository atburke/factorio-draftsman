# mining_drill.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    ModulesMixin,
    RequestItemsMixin,
    CircuitReadResourceMixin,
    CircuitConditionMixin,
    EnableDisableMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
)
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman import utils
from draftsman.warning import DraftsmanWarning, ItemLimitationWarning

from draftsman.data.entities import mining_drills
from draftsman.data import modules
from draftsman.data import items

from schema import SchemaError
import six
from typing import ClassVar
import warnings


class MiningDrill(
    ModulesMixin,
    RequestItemsMixin,
    CircuitReadResourceMixin,
    CircuitConditionMixin,
    LogisticConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
    Entity,
):
    """
    An entity that extracts resources from the environment.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **DirectionalMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **EnableDisableMixin._exports,
    #     **LogisticConditionMixin._exports,
    #     **CircuitConditionMixin._exports,
    #     **CircuitReadResourceMixin._exports,
    #     **RequestItemsMixin._exports,
    #     **ModulesMixin._exports,
    # }
    # fmt: on
    class Format(
        ModulesMixin.Format,
        RequestItemsMixin.Format,
        CircuitReadResourceMixin.Format,
        CircuitConditionMixin.Format,
        LogisticConditionMixin.Format,
        EnableDisableMixin.Format,
        ControlBehaviorMixin.Format,
        CircuitConnectableMixin.Format,
        DirectionalMixin.Format,
        Entity.Format
    ):
        class ControlBehavior(
            CircuitReadResourceMixin.ControlFormat,
            CircuitConditionMixin.ControlFormat,
            LogisticConditionMixin.ControlFormat,
            EnableDisableMixin.ControlFormat,
        ):
            pass

        control_behavior: ControlBehavior | None = ControlBehavior()

    def __init__(self, name=mining_drills[0], **kwargs):
        # type: (str, **dict) -> None
        super(MiningDrill, self).__init__(name, mining_drills, **kwargs)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

        del self.unused_args

    # =========================================================================

    # @ControlBehaviorMixin.control_behavior.setter
    # def control_behavior(self, value):
    #     # type: (dict) -> None
    #     try:
    #         self._control_behavior = signatures.MINING_DRILL_CONTROL_BEHAVIOR.validate(
    #             value
    #         )
    #     except SchemaError as e:
    #         six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @utils.reissue_warnings
    def set_item_request(self, item, amount):
        # type: (str, int) -> None
        # Make sure the item exists
        # if item not in items.raw:
        #     raise InvalidItemError(item)

        if item in items.raw and item not in modules.raw:
            warnings.warn(
                "Item '{}' cannot be placed in MiningDrill".format(item),
                ItemLimitationWarning,
                stacklevel=2,
            )

        # self._handle_module_slots(item, amount)

        super(MiningDrill, self).set_item_request(item, amount)

    # =========================================================================

    __hash__ = Entity.__hash__
