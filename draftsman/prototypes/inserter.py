# inserter.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    StackSizeMixin,
    CircuitReadHandMixin,
    InserterModeOfOperationMixin,
    CircuitConditionMixin,
    LogisticConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
)
from draftsman.constants import InserterModeOfOperation
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import inserters

from schema import SchemaError
import six
from typing import ClassVar
import warnings


class Inserter(
    StackSizeMixin,
    CircuitReadHandMixin,
    InserterModeOfOperationMixin,
    CircuitConditionMixin,
    LogisticConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
    Entity,
):
    """
    An entity that can move items between machines.

    .. NOTE::

        In Factorio, the ``Inserter`` prototype includes both regular and filter
        inserters. In Draftsman, inserters are split into two different classes,
        :py:class:`~.Inserter` and :py:class:`~.FilterInserter`
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **DirectionalMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **LogisticConditionMixin._exports,
    #     **CircuitConditionMixin._exports,
    #     **InserterModeOfOperationMixin._exports,
    #     **CircuitReadHandMixin._exports,
    #     **StackSizeMixin._exports,
    # }
    # fmt: on
    class Format(
        StackSizeMixin.Format,
        CircuitReadHandMixin.Format,
        InserterModeOfOperationMixin.Format,
        CircuitConditionMixin.Format,
        LogisticConditionMixin.Format,
        EnableDisableMixin.Format,
        ControlBehaviorMixin.Format,
        CircuitConnectableMixin.Format,
        DirectionalMixin.Format,
        Entity.Format,
    ):
        class ControlBehavior(
            StackSizeMixin.ControlFormat,
            CircuitReadHandMixin.ControlFormat,
            InserterModeOfOperationMixin.ControlFormat,
            CircuitConditionMixin.ControlFormat,
            LogisticConditionMixin.ControlFormat,
            EnableDisableMixin.ControlFormat,
        ):
            pass

        control_behavior: ControlBehavior | None = ControlBehavior()

    def __init__(self, name=inserters[0], **kwargs):
        # type: (str, **dict) -> None
        super(Inserter, self).__init__(name, inserters, **kwargs)

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
    #         self._control_behavior = signatures.INSERTER_CONTROL_BEHAVIOR.validate(
    #             value
    #         )
    #     except SchemaError as e:
    #         six.raise_from(DataFormatError(e), None)

    # =========================================================================

    __hash__ = Entity.__hash__
