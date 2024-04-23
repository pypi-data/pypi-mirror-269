#!/usr/bin/env python3
from __future__ import annotations

from typing import Mapping, Any, Iterator, Iterable
from collections import UserDict
from collections.abc import Set, KeysView, ItemsView, ValuesView


class ThickKey(Set):
    """A custom "key" for a Thick dict. Effectively a frozenset implementation
    with a custom repr."""

    def __init__(self, d: Any) -> None:
        """wraps around a frozenset, the input data can be
        any type, will be cast to a Collection"""
        if (isinstance(d, str) and len(d) > 1) or not isinstance(d, Iterable):
            d = (d,)
        self.data: frozenset[Any] = frozenset(d)
        super().__init__()

    def __contains__(self, key: Any) -> bool:
        return key in self.data

    def __iter__(self) -> Iterator[Any]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __hash__(self) -> int:
        """A ThickKey is a frozenset, thus it can (and must)
        implement __hash__"""
        return self._hash()

    def __repr__(self) -> str:
        """A custom __repr__ to show make the Thick{Keys | Values | Items}Views
        look better"""
        # This makes the Thick*Views look better
        return repr(tuple(self.data))


class Thick(UserDict):
    """A dictionary where each value is deduplicated.
    Effectively allows for mapping a Collection of values
    to one output"""

    #####################################
    # Modified from collections.UserDict
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    # Using UserDict's __init__ method works fine for us.

    def __or__(self, other: Any) -> Thick:
        if isinstance(other, UserDict | dict | Thick):
            new: Thick = self.copy()
            new.update(other)
            return new
        return NotImplemented

    def __ror__(self, other: Any) -> Thick:
        if isinstance(other, UserDict | dict | Thick):
            new: Thick = self.copy()
            new.update(other)
            return new
        return NotImplemented

    def __ior__(self, other: Any) -> Thick:
        if isinstance(other, UserDict | Thick | dict):
            k: Any
            v: Any
            for k, v in other.items():
                self[k] = v
            return self
        return NotImplemented

    def copy(self) -> Thick:
        if self.__class__ is Thick:
            return Thick(self.data.copy())
        import copy

        data: dict[frozenset[Any], Any] = self.data
        try:
            self.data = {}
            c: Any = copy.copy(self)
        finally:
            self.data = data
        # If this looks like "c" could, somehow, be unbound
        # That's because this is a word-for-word copy of
        # the copy implementation of UserDict, except for
        # substituting "UserDict" for "Thick" and adding
        # type hints. ymmv on using subclasses of Thick (or UserDict)
        # with this.
        c.update(self)
        return c

    def __contains__(self, key: Any) -> bool:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        return check_key in self.keys()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Modified from collections.UserDict
    #####################################
    # Modified from collections.abc.MutableMapping
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __getitem__(self, key: Any) -> Any:
        """Very similar to the reference implementation,
        simply changed for type hinting and to get an entire
        key from a partial key when necessary"""
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        if check_key in self.keys():
            whole_key: ThickKey = self.get_entire_key(check_key)
            return self.data[whole_key]

        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)

        raise KeyError(key)

    def __setitem__(self, key: Any, item: Any) -> None:
        """By far the most involved method of the data structure.
        Effectively works to ensure that we retain the invariant
        nature of the data structure: each value is entered once,
        the keys are added or removed to the set as required."""
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        current_key: ThickKey
        current_value: Any
        # First, if the item is already in this
        if item in self.values():
            for current_key, current_value in self.items():
                if item == current_value:
                    # If the given key is not a subset of the current key
                    if not (check_key <= current_key):
                        # Create a new key as the union of the two
                        # Use only this key
                        # (The cast to ThickKey is technially redundant,
                        # But mypy complains otherwise)
                        new_key: ThickKey = ThickKey(current_key | check_key)
                        del self.data[current_key]
                        self.data[new_key] = current_value
                    return

        # Otherwise, the item is new
        else:
            mutable_new_key: set[Any]
            k: Any
            for current_key, current_value in self.items():
                # If the desired key is already partially (or fully)
                # In the keys
                if check_key <= current_key:
                    mutable_new_key = set(current_key)
                    # Remove all the desired values from the
                    # old key
                    for k in check_key:
                        mutable_new_key.remove(k)
                    del self.data[current_key]
                    # If there are still values in the old key,
                    # reset it
                    if len(mutable_new_key) > 0:
                        self.data[ThickKey(mutable_new_key)] = current_value
                    self.data[check_key] = item
                    return

                # This is what happens when there are overlapping items
                # but check_key is not a subset of current_key
                else:
                    # (The cast to ThickKey is technially redundant,
                    # But mypy complains otherwise)
                    key_intersection: ThickKey = ThickKey(check_key & current_key)
                    if len(key_intersection) != 0:
                        mutable_new_key = set(current_key)
                        # Remove any values in the intersection that are
                        # in the current_key
                        for k in key_intersection:
                            if k in mutable_new_key:
                                mutable_new_key.remove(k)

                        # The old version gets deleted
                        # The given check_key is set to the desired item
                        # The remaining values from the current_key are
                        # in new_key and set to the current_value
                        del self.data[check_key]
                        self.data[ThickKey(mutable_new_key)] = current_value
                        self.data[check_key] = item
                        return

        # If we've fallen through here, the value is not already in the Thick dict
        # And the given key has no intersection with any key already in the Thick dict
        # Thus, we just set the new value
        self.data[check_key] = item

    def __delitem__(self, key: Any) -> None:
        """Very similar to the reference implementation,
        simply changed for type hinting and to get an entire
        key from a partial key when necessary"""
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        if check_key in self.data:
            del self.data[check_key]
            return

        if check_key in self.keys():
            whole_key: ThickKey = self.get_entire_key(check_key)
            # (The cast to ThickKey is technially redundant,
            # But mypy complains otherwise)
            remaining_keys: ThickKey = ThickKey(whole_key - check_key)
            val: Any = self.data[whole_key]
            del self.data[whole_key]
            self.data[remaining_keys] = val
            return

        # If part of all of the check_key is not
        # already in the Thick dict, it's a key error
        raise KeyError(key)

    def get_entire_key(self, key: Any) -> ThickKey:
        """Given a partial key, return the entire key."""
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        current_key: ThickKey
        for current_key in self.keys():
            if check_key <= current_key:
                return current_key

        raise KeyError(key)

    def delete_entire_key(self, key: Any) -> None:
        """Given a partial (or full) key, remove the entire
        key and its value"""
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        # If any part of it is there, remove the whole thing
        if check_key in self.keys():
            whole_key: ThickKey = self.get_entire_key(check_key)
            del self.data[whole_key]
            return

        raise KeyError(key)

    def reverse(self) -> Thick:
        """Because the Thick is required to have exactly one
        instance of each value, it is easy to create a "reversed"
        Thick, where the values become keys, and keys values
        """
        new: Thick = Thick()
        key: ThickKey
        value: Any
        for key, value in self.items():
            new[value] = key

        return new

    def thin(self) -> dict[Any, Any]:
        """Get the "thin" (i.e., not Thick) dictionary from the Thick. In essence, this "reduplicates" the dictionary."""
        thin_dict: dict[Any, Any] = {}
        for key, value in self.items():
            for k in key:
                thin_dict[k] = value

        return thin_dict

    def values(self) -> ThickValuesView:
        return ThickValuesView(self)

    def keys(self) -> ThickKeysView:
        return ThickKeysView(self)

    def items(self) -> ThickItemsView:
        return ThickItemsView(self)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Modified from collections.abc.MutableMapping
    #####################################


class ThickKeysView(KeysView):
    """A simple KeysView for this type of mapping with a custom repr"""

    # Type Hint for mypy
    _mapping: Thick

    def __contains__(self, key: Any) -> bool:
        """This implementation is very important. By
        checking in here on if an input key is either equal to
        or a subset of the mapping's keys."""
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        # Rather than repeating logic, we do this once here:

        # It's probably more inefficient to check the whole key and then
        # check each key in turn. Using a <= with the sets, we can just do
        # one for-loop, O(n) in the size of the Thick dict.
        k: ThickKey
        for k in self._mapping.keys():
            if check_key <= k:
                return True

        return False

    def __repr__(self):
        """Similar to a dict_keys __repr__"""
        return f"{self.__class__.__name__}({list(self._mapping.data.keys())})"


class ThickValuesView(ValuesView):
    """A simple ValuesView for this type of mapping with a custom repr"""

    def __repr__(self):
        """Similar to a dict_values __repr__"""
        return f"{self.__class__.__name__}({list(self._mapping.data.values())})"


class ThickItemsView(ItemsView):
    """A simple ItemsView for this type of mapping with a custom repr"""

    def __repr__(self):
        """Similar to a dict_items __repr__"""
        return f"{self.__class__.__name__}({list(zip(self._mapping.data.keys(), self._mapping.data.values()))})"
