# request_filters.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.signatures import RequestFilters
from draftsman.data import items
from draftsman.error import InvalidItemError, DataFormatError

from pydantic import BaseModel, ValidationError
import six

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no coverage
    from draftsman.classes.entity import Entity


class RequestFiltersMixin(object):
    """
    Used to allow Logistics Containers to request items from the Logistic
    network.
    """

    # _exports = {
    #     "request_filters": {
    #         "format": "TODO",
    #         "description": "A list of all items requested by this entity",
    #         "required": lambda x: x is not None,
    #     }
    # }
    class Format(BaseModel):
        request_filters: RequestFilters | None = None

    def __init__(self, name, similar_entities, **kwargs):
        # type: (str, list[str], **dict) -> None
        super(RequestFiltersMixin, self).__init__(name, similar_entities, **kwargs)

        self.request_filters = None

        if "request_filters" in kwargs:
            self.set_request_filters(kwargs["request_filters"])
            self.unused_args.pop("request_filters")
        # self._add_export("request_filters", lambda x: x is not None)

    # =========================================================================

    @property
    def request_filters(self):
        # type: () -> list[dict]
        """
        TODO
        """
        return self._root.get("request_filters", None)
    
    @request_filters.setter
    def request_filters(self, value):
        # type: (list[dict]) -> None
        if value is None:
            self._root.pop("request_filters", None)
        else:
            self._root["request_filters"] = value

    # =========================================================================

    def set_request_filter(self, index, item, count=None):
        # type: (int, str, int) -> None
        """
        Sets the request filter at a particular index to request an amount of a
        certain item. Factorio imposes that an Entity can only have 1000 active
        requests at the same time.

        :param index: The index of the item request.
        :param item: The item name to request, or ``None``.
        :param count: The amount to request. If set to ``None``, it defaults to
            the stack size of ``item``.

        :exception TypeError: If ``index`` is not an ``int``, ``item`` is not a
            ``str`` or ``None``, or ``count`` is not an ``int``.
        :exception InvalidItemError: If ``item`` is not a valid item name.
        :exception IndexError: If ``index`` is not in the range ``[0, 1000)``.
        """
        # try: # TODO
        #     index = signatures.INTEGER.validate(index)
        #     item = signatures.STRING_OR_NONE.validate(item)
        #     count = signatures.INTEGER_OR_NONE.validate(count)
        # except SchemaError as e:
        #     six.raise_from(TypeError(e), None)

        # if item is not None and item not in items.raw:
        #     raise InvalidItemError("'{}'".format(item))
        if not 0 <= index < 1000:
            raise IndexError("Filter index ({}) not in range [0, 1000)".format(index))
        if count is None:  # default count to the item's stack size
            count = 0 if item is None else items.raw[item]["stack_size"]
        if count < 0:
            raise ValueError("Filter count ({}) must be positive".format(count))

        if self.request_filters is None:
            self.request_filters = []

        # Check to see if filters already contains an entry with the same index
        for i, filter in enumerate(self.request_filters):
            if filter["index"] == index + 1:  # Index already exists in the list
                if item is None:  # Delete the entry
                    del self.request_filters[i]
                else:  # Set the new name + value
                    self.request_filters[i]["name"] = item
                    self.request_filters[i]["count"] = count
                return

        # If no entry with the same index was found
        self.request_filters.append({"index": index + 1, "name": item, "count": count})

    def set_request_filters(self, filters):
        # type: (list) -> None
        """
        Sets all the request filters of the Entity, where filters is of the
        format::

            [(item_1, count_1), (item_2, count_2), ...]

        where ``item_x`` is a ``str`` name and ``count_x`` is a positive integer.

        :param filters: The request filters to set.

        :exception DataFormatError: If ``filters`` does not match the format
            specified above.
        :exception InvalidItemError: If ``item_x`` is not a valid item name.
        """
        # Validate filters
        try:
            filters = RequestFilters(root=filters).model_dump(by_alias=True, exclude_none=True, exclude_defaults=True)
        except ValidationError as e:
            six.raise_from(DataFormatError(e), None)

        # Make sure the items are items
        # for item in filters:
        #     if item["name"] not in items.raw:
        #         raise InvalidItemError(item["name"])

        print(filters)

        self.request_filters = []
        for i in range(len(filters)):
            self.set_request_filter(i, filters[i]["name"], filters[i]["count"])

    def merge(self, other):
        # type: (Entity) -> None
        super(RequestFiltersMixin, self).merge(other)

        self.request_filters = other.request_filters

    # =========================================================================

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.request_filters == other.request_filters
