# deconstruction_planner.py
# -*- encoding: utf-8 -*-

"""
.. code-block:: python

    {
        "deconstruction_planner": {
            "item": "deconstruction-planner", # The associated item with this structure
            "label": str, # A user given name for this deconstruction planner
            "version": int, # The encoded version of Factorio this planner was created 
                            # with/designed for (64 bits)
            "settings": {
                "entity_filter_mode": int, # 0 = Whitelist, 1 = Blacklist
                "entity_filters": [ # A list of entities to deconstruct
                    {
                        "name": str, # Name of the entity
                        "index": int # Index of the entity in the list in range [1, 30]
                    },
                    ... # Up to 30 filters total
                ]
                "trees_and_rocks_only": bool, # Self explanatory, disables everything 
                                              # else
                "tile_filter_mode": int, # 0 = Whitelist, 1 = Blacklist
                "tile_filters": [ # A list of tiles to deconstruct
                    {
                        "name": str, # Name of the tile
                        "index": int # Index of the tile in the list in range [1, 30]
                    },
                    ... # Up to 30 filters total
                ]
                "tile_selection_mode": int, # 0 = Normal, 1 = Always, 2 = Never, 
                                            # 3 = Only
                "description": str, # A user given description for this deconstruction 
                                    # planner
                "icons": [ # A set of signals to act as visual identification
                    {
                        "signal": {"name": str, "type": str}, # Name and type of signal
                        "index": int, # In range [1, 4], starting top-left and moving across
                    },
                    ... # Up to 4 icons total
                ],
            }
        }
    }
"""

from __future__ import unicode_literals

from draftsman import __factorio_version_info__
from draftsman.classes.blueprintable import Blueprintable
from draftsman.classes.exportable import ValidationResult
from draftsman.constants import FilterMode, TileSelectionMode
from draftsman.data import entities, tiles
from draftsman.error import DataFormatError, InvalidItemError
from draftsman.warning import IndexWarning, UnrecognizedElementWarning
from draftsman.signatures import BaseModel, Icons, EntityFilter, TileFilter
from draftsman import utils
from draftsman.warning import DraftsmanWarning

from pydantic import Field
import six
from typing import Union, Literal
import warnings


class DeconstructionPlanner(Blueprintable):
    """
    Handles the deconstruction of entities. Has functionality to only select
    certain entities or tiles, as well as only natural objects like trees and
    rocks.
    """

    # =========================================================================
    # Format
    # =========================================================================

    class Format(BaseModel):
        class DeconstructionPlannerObject(BaseModel):
            item: Literal["deconstruction-planner"]
            label: str | None = None
            version: int | None = Field(None, ge=0, lt=2**64)

            class Settings(BaseModel):
                description: str | None = None
                icons: Icons | None = None

                entity_filter_mode: FilterMode | None = None
                entity_filters: list[EntityFilter] | None = None
                trees_and_rocks_only: bool | None = None
                
                tile_filter_mode: FilterMode | None = None
                tile_filters: list[TileFilter] | None = None
                tile_selection_mode: TileSelectionMode | None = None

            settings: Settings | None = Settings()

        deconstruction_planner: DeconstructionPlannerObject
        index: int | None = Field(None, description="Only present when inside a BlueprintBook") # TODO: dimension

    # =========================================================================
    # Constructors
    # =========================================================================

    @utils.reissue_warnings
    def __init__(self, deconstruction_planner=None, unknown="error"):
        # type: (Union[str, dict], str) -> None
        """
        TODO
        """
        super(DeconstructionPlanner, self).__init__(
            # format=DeconstructionPlannerModel,
            root_item="deconstruction_planner",
            item="deconstruction-planner",
            init_data=deconstruction_planner,
            unknown=unknown,
        )

    @utils.reissue_warnings
    def setup(self, unknown="error", **kwargs):
        self._root = {}
        self._root["settings"] = {}

        # Item (type identifier)
        self._root["item"] = "deconstruction-planner"
        kwargs.pop("item", None)

        self.label = kwargs.pop("label", None)

        if "version" in kwargs:
            self.version = kwargs.pop("version")
        else:
            self.version = utils.encode_version(*__factorio_version_info__)

        settings = kwargs.pop("settings", None)
        if settings is not None:
            self.entity_filter_mode = settings.pop("entity_filter_mode", None)
            self.entity_filters = settings.pop("entity_filter_mode", None)
            self.trees_and_rocks_only = settings.pop("trees_and_rocks_only", None)

            self.tile_filter_mode = settings.pop("tile_filter_mode", None)
            self.tile_filters = settings.pop("tile_filters", None)
            self.tile_selection_mode = settings.pop("tile_selection_mode", None)

            self.description = settings.pop("description", None)
            self.icons = settings.pop("icons", None)

        # Issue warnings for any keyword not recognized by UpgradePlanner
        for unused_arg in kwargs:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def entity_filter_mode(self):
        # type: () -> FilterMode
        """
        The method of filtering entities for deconstruction. Can be either ``0``
        (whitelist) or ``1`` (blacklist).

        :getter: Gets the entity filter mode, or ``None`` if not set.
        :setter: Sets the entity filter mode. Deletes the key if set to ``None``.
        :type: :py:data:`.FilterMode`

        :raises ValueError: If not set to an valid :py:data:`.FilterMode` or
            ``None``.
        """
        return self._root["settings"].get("entity_filter_mode", None)

    @entity_filter_mode.setter
    def entity_filter_mode(self, value):
        # type: (FilterMode) -> None
        if value is None:
            self._root["settings"].pop("entity_filter_mode", None)
        else:
            self._root["settings"]["entity_filter_mode"] = FilterMode(value)

    # =========================================================================

    @property
    def entity_filters(self):
        # type: () -> list[dict]
        """
        The list of entity filters.
        TODO
        """
        return self._root["settings"].get("entity_filters", None)

    @entity_filters.setter
    def entity_filters(self, value):
        # type: (list[dict]) -> None
        # TODO: what if index >= 30?
        if value is None:
            self._root["settings"].pop("entity_filters", None)
        else:
            self._root["settings"]["entity_filters"] = value

    # =========================================================================

    @property
    def trees_and_rocks_only(self):
        # type: () -> bool
        """
        Whether or not to only deconstruct natural entities, such as trees and
        rocks.

        :getter: Gets the flag, or returns ``None`` if not set.
        :setter: Sets the flag, or deletes the key if set to ``None``.
        :type: ``bool``

        :raises TypeError: If set to anything other than a ``bool`` or ``None``.
        """
        return self._root["settings"].get("trees_and_rocks_only", None)

    @trees_and_rocks_only.setter
    def trees_and_rocks_only(self, value):
        # type: (bool) -> None
        if value is None:
            self._root["settings"].pop("trees_and_rocks_only", None)
        elif isinstance(value, bool):
            self._root["settings"]["trees_and_rocks_only"] = value
        else:
            raise TypeError("'trees_and_rocks_only' must be either a bool or None")

    # =========================================================================

    @property
    def tile_filter_mode(self):
        # type: () -> FilterMode
        """
        The method of filtering tiles for deconstruction. Can be either ``0``
        (whitelist) or ``1`` (blacklist).

        :getter: Gets the tile filter mode, or ``None`` if not set.
        :setter: Sets the tile filter mode. Deletes the key if set to ``None``.
        :type: :py:data:`.FilterMode`

        :raises ValueError: If not set to an valid :py:data:`.FilterMode` or
            ``None``.
        """
        return self._root["settings"].get("tile_filter_mode", None)

    @tile_filter_mode.setter
    def tile_filter_mode(self, value):
        # type: (FilterMode) -> None
        if value is None:
            self._root["settings"].pop("tile_filter_mode", None)
        else:
            self._root["settings"]["tile_filter_mode"] = FilterMode(value)

    # =========================================================================

    @property
    def tile_filters(self):
        # type: () -> list[dict]
        """
        The list of tile filters.
        TODO
        """
        return self._root["settings"].get("tile_filters", None)

    @tile_filters.setter
    def tile_filters(self, value):
        # type: (list[dict]) -> None
        if value is None:
            self._root["settings"].pop("tile_filters", None)
        else:
            self._root["settings"]["tile_filters"] = value

    # TODO: set_tile_filters() function

    # =========================================================================

    @property
    def tile_selection_mode(self):
        # type: () -> TileSelectionMode
        """
        The method of filtering entities for deconstruction. Valid modes are:

        0. ``NORMAL`` (default)
        1. ``ALWAYS``
        2. ``NEVER``
        3. ``ONLY``

        :getter: Gets the entity filter mode, or ``None`` if not set.
        :setter: Sets the entity filter mode. Deletes the key if set to ``None``.
        :type: :py:data:`.TileSelectionMode`

        :raises ValueError: If not set to a valid :py:data:`.TileSelectionMode`
            or ``None``.
        """
        return self._root["settings"].get("tile_selection_mode", None)

    @tile_selection_mode.setter
    def tile_selection_mode(self, value):
        # type: (TileSelectionMode) -> None
        if value is None:
            self._root["settings"].pop("tile_selection_mode", None)
        else:
            self._root["settings"]["tile_selection_mode"] = TileSelectionMode(value)

    # =========================================================================
    # Utility functions
    # =========================================================================

    def set_entity_filter(self, index, name):
        # type: (int, str) -> None
        """
        Sets an entity filter in the list of entity filters. Appends the new one
        to the end of the list regardless of the ``index``. If ``index`` is
        already occupied with a different filter it is overwritten with the new
        one; does nothing if the exact filter already exists within
        :py:attr:`.entity_filters`.

        :param index: The index to set the new filter at.
        :param name: The name of the entity to filter for deconstruction.
        """
        if self.entity_filters is None:
            self.entity_filters = []

        # Check if index is ouside the range of the max filter slots
        # if not 0 <= index < 30:
        #     raise IndexError(
        #         "Index {} exceeds the maximum number of entity filter slots (30)".format(
        #             index
        #         )
        #     )

        # Check to see that `name` is a valid entity
        # TODO

        for i in range(len(self.entity_filters)):
            filter = self.entity_filters[i]
            if filter["index"] == index + 1:
                if name is None:
                    del self.entity_filters[i]
                else:
                    filter["name"] = name
                return

        # Otherwise its unique; add to list
        self.entity_filters.append({"index": index + 1, "name": name})

    def set_entity_filters(self, *entity_names: list[str]):
        """
        TODO
        """
        for i, entity_name in enumerate(entity_names):
            self.set_entity_filter(i, entity_name)

    def set_tile_filter(self, index, name):
        # type: (int, str) -> None
        """
        Sets a tile filter in the list of tile filters. Appends the new one
        to the end of the list regardless of the ``index``. If ``index`` is
        already occupied with a different filter it is overwritten with the new
        one; does nothing if the exact filter already exists within
        :py:attr:`.tile_filters`.

        :param index: The index to set the new filter at.
        :param name: The name of the tile to filter for deconstruction.
        """
        if self.tile_filters is None:
            self.tile_filters = []

        # Check if `index` is ouside the range of the max filter slots
        # if not 0 <= index < 30:
        #     raise IndexError(
        #         "Index {} exceeds the maximum number of tile filter slots (30)".format(
        #             index
        #         )
        #     )

        # Check to see that `name` is a valid tile
        # TODO

        for i in range(len(self.tile_filters)):
            filter = self.tile_filters[i]
            if filter["index"] == index + 1:
                if name is None:
                    del self.tile_filters[i]
                else:
                    filter["name"] = name
                return

        # Otherwise its unique; add to list
        self.tile_filters.append({"index": index + 1, "name": name})

    def set_tile_filters(self, *tile_names: list[str]):
        """
        TODO
        """
        for i, tile_name in enumerate(tile_names):
            self.set_tile_filter(i, tile_name)

    # =========================================================================

    def validate(self):
        """
        TODO
        """
        if self.is_valid:
            return
        
        # TODO: wrap with DataFormatError or similar
        # TODO: this is a bit confusingly named, but it shouldn't matter for
        # the end user
        DeconstructionPlanner.Format.DeconstructionPlannerObject.model_validate(self._root)

        super().validate()

    def inspect(self) -> ValidationResult:
        result = super().inspect()

        # By nature of necessity, we must ensure that all members of upgrade
        # planner are in a correct and known format, so we must call:
        try:
            self.validate()
        except Exception as e:
            # If validation fails, it's in a format that we do not expect; and
            # therefore unreasonable for us to assume that we can continue
            # checking for issues relating to that non-existent format.
            # Therefore, we add the errors to the error list and early exit
            # TODO: figure out the proper way to reraise
            result.error_list.append(DataFormatError(str(e)))
            return result

        for entity_filter in self.entity_filters:
            if not 0 <= entity_filter["index"] < 30:
                result.warning_list.append(
                    IndexWarning(
                        "Index of entity_filter '{}' ({}) exceeds the maximum number of tile filter slots (30)".format(
                            entity_filter["name"], entity_filter["index"]
                        )
                    )
                )
            
            if entity_filter["name"] not in entities.raw:
                result.warning_list.append(
                    UnrecognizedElementWarning(
                        "Unrecognized entity '{}'".format(entity_filter["name"])
                    )
                )

        for tile_filter in self.tile_filters:
            if not 0 <= tile_filter["index"] < 30:
                result.warning_list.append(
                    IndexWarning(
                        "Index of entity_filter '{}' ({}) exceeds the maximum number of tile filter slots (30)".format(
                            tile_filter["name"], tile_filter["index"]
                        )
                    )
                )
            
            if tile_filter["name"] not in tiles.raw:
                result.warning_list.append(
                    UnrecognizedElementWarning(
                        "Unrecognized tile '{}'".format(entity_filter["name"])
                    )
                )

        return result

    def to_dict(self):
        out_model = DeconstructionPlanner.Format.model_construct(
            **{self._root_item: self._root}, _recursive=True
        )

        print(out_model)

        # We then create an output dict
        out_dict = out_model.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude_defaults=True,
            warnings=False,  # Ignore warnings until model_construct is recursive
        )

        return out_dict
