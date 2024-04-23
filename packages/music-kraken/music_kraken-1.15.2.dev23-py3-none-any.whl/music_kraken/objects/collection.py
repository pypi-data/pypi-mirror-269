from __future__ import annotations

from collections import defaultdict
from typing import TypeVar, Generic, Dict, Optional, Iterable, List, Iterator, Tuple, Generator, Union, Any
from .parents import OuterProxy
from ..utils import object_trace

T = TypeVar('T', bound=OuterProxy)


class Collection(Generic[T]):
    __is_collection__ = True

    _data: List[T]

    _indexed_values: Dict[str, set]
    _indexed_to_objects: Dict[any, list]

    shallow_list = property(fget=lambda self: self.data)

    def __init__(
            self,
            data: Optional[Iterable[T]] = None,
            sync_on_append: Dict[str, Collection] = None,
            append_object_to_attribute: Dict[str, T] = None,
            extend_object_to_attribute: Dict[str, Collection] = None,
    ) -> None:
        self._collection_for: dict = dict()

        self._contains_ids = set()
        self._data = []

        # List of collection attributes that should be modified on append
        # Key: collection attribute (str) of appended element
        # Value: main collection to sync to
        self.append_object_to_attribute: Dict[str, T] = append_object_to_attribute or {}
        self.extend_object_to_attribute: Dict[str, Collection[T]] = extend_object_to_attribute or {}
        self.sync_on_append: Dict[str, Collection] = sync_on_append or {}

        self._id_to_index_values: Dict[int, set] = defaultdict(set)
        
        # This is to cleanly unmap previously mapped items by their id
        self._indexed_from_id: Dict[int, Dict[str, Any]] = defaultdict(dict)
        # this is to keep track and look up the actual objects
        self._indexed_values: Dict[str, Dict[Any, T]] = defaultdict(dict)

        self.extend(data)

    def __repr__(self) -> str:
        return f"Collection({id(self)})"

    def _map_element(self, __object: T, from_map: bool = False):
        self._unmap_element(__object.id)

        self._indexed_from_id[__object.id]["id"] = __object.id
        self._indexed_values["id"][__object.id] = __object

        for name, value in __object.indexing_values:
            if value is None or value == __object._inner._default_values.get(name):
                continue

            self._indexed_values[name][value] = __object
            self._indexed_from_id[__object.id][name] = value

    def _unmap_element(self, __object: Union[T, int]):
        obj_id = __object.id if isinstance(__object, OuterProxy) else __object

        if obj_id not in self._indexed_from_id:
            return

        for name, value in self._indexed_from_id[obj_id].items():
            if value in self._indexed_values[name]:
                del self._indexed_values[name][value]

        del self._indexed_from_id[obj_id]

    def _find_object(self, __object: T) -> Optional[T]:
        for name, value in __object.indexing_values:
            if value in self._indexed_values[name]:
                return self._indexed_values[name][value]

    def append(self, __object: Optional[T], already_is_parent: bool = False, from_map: bool = False):
        """
        If an object, that represents the same entity exists in a relevant collection,
        merge into this object. (and remap)
        Else append to this collection.

        :param __object:
        :param already_is_parent:
        :param from_map:
        :return:
        """

        if __object is None:
            return

        existing_object = self._find_object(__object)

        if existing_object is None:
            # append
            self._data.append(__object)
            self._map_element(__object)

            for collection_attribute, child_collection in self.extend_object_to_attribute.items():
                __object.__getattribute__(collection_attribute).extend(child_collection)

            for attribute, new_object in self.append_object_to_attribute.items():
                __object.__getattribute__(attribute).append(new_object)

            # only modify collections if the object actually has been appended
            for attribute, a in self.sync_on_append.items():
                b = __object.__getattribute__(attribute)
                object_trace(f"Syncing [{a}{id(a)}] = [{b}{id(b)}]")

                data_to_extend = b.data

                a._collection_for.update(b._collection_for)
                for synced_with, key in b._collection_for.items():
                    synced_with.__setattr__(key, a)

                a.extend(data_to_extend)


        else:
            # merge only if the two objects are not the same
            if existing_object.id == __object.id:
                return

            old_id = existing_object.id

            existing_object.merge(__object)

            if existing_object.id != old_id:
                self._unmap_element(old_id)

            self._map_element(existing_object)            

    def extend(self, __iterable: Optional[Generator[T, None, None]]):
        if __iterable is None:
            return

        for __object in __iterable:
            self.append(__object)

    @property
    def data(self) -> List[T]:
        return list(self.__iter__())

    def __len__(self) -> int:
        return len(self._data)

    @property
    def empty(self) -> bool:
        return self.__len__() <= 0

    def __iter__(self) -> Iterator[T]:
        yield from self._data

    def __merge__(self, __other: Collection, override: bool = False):
        self.extend(__other)

    def __getitem__(self, item: int):
        return self._data[item]
