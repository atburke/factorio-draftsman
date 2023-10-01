# electric_energy_interface.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import electric_energy_interfaces

import six
import warnings


class ElectricEnergyInterface(Entity):
    """
    An entity that interfaces with an electrical grid.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     "buffer_size": {
    #         "format": "int",
    #         "description": "How much energy this interface can store",
    #         "required": lambda x: x is not None,
    #     },
    #     "power_production": {
    #         "format": "int",
    #         "description": "How much energy this interface produces per tick",
    #         "required": lambda x: x is not None,
    #     },
    #     "power_usage": {
    #         "format": "int",
    #         "description": "How much energy this interface consumes per tick",
    #         "required": lambda x: x is not None,
    #     },
    # }
    # fmt: on
    class Format(Entity.Format):
        buffer_size: int | None = None # TODO: dimension
        power_production: int | None = None # TODO: dimension
        power_usage: int | None = None # TODO: dimension

    def __init__(self, name=electric_energy_interfaces[0], **kwargs):
        # type: (str, **dict) -> None
        super(ElectricEnergyInterface, self).__init__(
            name, electric_energy_interfaces, **kwargs
        )

        self.buffer_size = None  # TODO: default
        if "buffer_size" in kwargs:
            self.buffer_size = kwargs["buffer_size"]
            self.unused_args.pop("buffer_size")
        # self._add_export("buffer_size", lambda x: x is not None)

        self.power_production = None  # TODO: default
        if "power_production" in kwargs:
            self.power_production = kwargs["power_production"]
            self.unused_args.pop("power_production")
        # self._add_export("power_production", lambda x: x is not None)

        self.power_usage = None  # TODO: default
        if "power_usage" in kwargs:
            self.power_usage = kwargs["power_usage"]
            self.unused_args.pop("power_usage")
        # self._add_export("power_usage", lambda x: x is not None)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

        del self.unused_args

    # =========================================================================

    @property
    def buffer_size(self):
        # type: () -> int
        """
        The amount of electrical energy to store in Watts.

        :getter: Gets the value of the buffer.
        :setter: Sets the value of the buffer.
        :type: ``int``

        :exception TypeError: If set to anything other than an ``int`` or
            ``None``.
        """
        return self._root.get("buffer_size", None)

    @buffer_size.setter
    def buffer_size(self, value):
        # type: (int) -> None
        if value is None:
            self._root.pop("buffer_size", None)
        else:
            self._root["buffer_size"] = value

    # =========================================================================

    @property
    def power_production(self):
        # type: () -> int
        """
        The amount of electrical energy to create each tick in Watts.

        :getter: Gets how much to make.
        :setter: Sets how much to make.
        :type: ``int``

        :exception TypeError: If set to anything other than an ``int`` or
            ``None``.
        """
        return self._root.get("power_production", None)

    @power_production.setter
    def power_production(self, value):
        # type: (int) -> None
        if value is None:
            self._root.pop("power_production", None)
        else:
            self._root["power_production"] = value

    # =========================================================================

    @property
    def power_usage(self):
        # type: () -> int
        """
        The amount of electrical energy to use each tick in Watts.

        :getter: Gets how much to use.
        :setter: Sets how much to use.
        :type: ``int``

        :exception TypeError: If set to anything other than an ``int`` or
            ``None``.
        """
        return self._root.get("power_usage", None)

    @power_usage.setter
    def power_usage(self, value):
        # type: (int) -> None
        if value is None:
            self._root.pop("power_usage", None)
        else:
            self._root["power_usage"] = value

    # =========================================================================

    def merge(self, other):
        # type: (ElectricEnergyInterface) -> None
        super(ElectricEnergyInterface, self).merge(other)

        self.buffer_size = other.buffer_size
        self.power_production = other.power_production
        self.power_usage = other.power_usage

    # =========================================================================

    __hash__ = Entity.__hash__

    def __eq__(self, other) -> bool:
        return (
            super().__eq__(other)
            and self.buffer_size == other.buffer_size
            and self.power_production == other.power_production
            and self.power_usage == other.power_usage
        )
