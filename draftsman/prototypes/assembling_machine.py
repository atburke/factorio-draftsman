# assembling_machine.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import RequestItemsMixin, RecipeMixin
from draftsman.error import InvalidItemError
from draftsman.warning import (
    DraftsmanWarning,
    ModuleLimitationWarning,
    ItemLimitationWarning,
)

from draftsman.data.entities import assembling_machines
from draftsman.data import modules
from draftsman.data import items
from draftsman.data import recipes

import warnings


class AssemblingMachine(RecipeMixin, RequestItemsMixin, Entity):
    def __init__(self, name=assembling_machines[0], **kwargs):
        # type: (str, **dict) -> None
        super(AssemblingMachine, self).__init__(name, assembling_machines, **kwargs)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

    def set_item_request(self, item, amount):
        # type: (str, int) -> None
        """
        Overwritten
        """
        # Make sure the item exists
        if item not in items.raw:
            raise InvalidItemError("'{}'".format(item))

        # If the item is a module
        if item in modules.raw:
            # Check to make sure the recipe within the module's limitations
            # (If it has any)
            module = modules.raw[item]
            if "limitation" in module:
                if self.recipe is not None and self.recipe not in module["limitation"]:
                    tooltip = module.get("limitation_message_key", "no message key")
                    warnings.warn(
                        "Cannot use module '{}' with recipe '{}' ({})".format(
                            item, self.recipe, tooltip
                        ),
                        ModuleLimitationWarning,
                        stacklevel=2,
                    )

        # Make sure the item is one of the input ingredients for the recipe
        elif self.recipe is not None:
            ingredients = recipes.get_recipe_ingredients(self.recipe)

            if item not in ingredients:
                warnings.warn(
                    "Cannot request items that the recipe '{}' doesn't use ({})".format(
                        self.recipe, item
                    ),
                    ItemLimitationWarning,
                    stacklevel=2,
                )

        super(AssemblingMachine, self).set_item_request(item, amount)
