# filter_inserter.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    FiltersMixin,
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
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import filter_inserters

from schema import SchemaError
import six
from typing import Literal
import warnings


class FilterInserter(
    FiltersMixin,
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
    An entity that can move items between machines, and has the ability to only
    move specific items.

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
    #     **FiltersMixin._exports,
    #     "filter_mode": {
    #         "format": "'whitelist' or 'blacklist'",
    #         "description": "Whether or not to invert the item filters specified",
    #         "required": lambda x: x is not None,
    #     },
    # }
    # fmt: on
    class Format(
        FiltersMixin.Format,
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

        filter_mode: Literal["whitelist", "blacklist"] | None = None

    def __init__(self, name=filter_inserters[0], **kwargs):
        # type: (str, **dict) -> None
        super(FilterInserter, self).__init__(name, filter_inserters, **kwargs)

        self.filter_mode = None
        if "filter_mode" in kwargs:
            self.filter_mode = kwargs["filter_mode"]
            self.unused_args.pop("filter_mode")
        # self._add_export("filter_mode", lambda x: x is not None)

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
    #         self._control_behavior = (
    #             signatures.FILTER_INSERTER_CONTROL_BEHAVIOR.validate(value)
    #         )
    #     except SchemaError as e:
    #         six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def filter_mode(self):
        # type: () -> str
        """
        The mode that the filter is set to. Can be either ``"whitelist"`` or
        ``"blacklist"``.

        :getter: Gets the filter mode.
        :setter: Sets the filter mode.
        :type: ``str``

        :exception ValueError: If set to a ``str`` that is neither ``"whitelist"``
            nor ``"blacklist"``.
        :exception TypeError: If set to anything other than a ``str`` or ``None``.
        """
        return self._root.get("filter_mode", None)

    @filter_mode.setter
    def filter_mode(self, value):
        # type: (str) -> None
        # TODO: evaluate when this check should take place
        if value is None:
            self._root.pop("filter_mode", None)
        elif value in {"whitelist", "blacklist"}:
            self._root["filter_mode"] = value
        else:
            raise ValueError("'filter_mode' must be one of {'whitelist', 'blacklist'} or None")

    # =========================================================================

    def merge(self, other):
        # type: (FilterInserter) -> None
        super(FilterInserter, self).merge(other)

        self.filter_mode = other.filter_mode

    # =========================================================================

    __hash__ = Entity.__hash__

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.filter_mode == other.filter_mode
