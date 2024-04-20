from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Type, Union

if sys.version_info >= (3, 9):  # pragma: no cover
    from collections.abc import Generator, Mapping, MutableMapping, MutableSequence, Sequence
else:  # pragma: no cover
    from typing import Generator, Mapping, MutableMapping, MutableSequence, Sequence

from .constructor import Constructor
from .data import Data

if TYPE_CHECKING:  # pragma: no cover
    from yaml.cyaml import _CLoader as YAML_CLoader
    from yaml.loader import _Loader as YAML_Loader


__all__ = ["load", "lazy_load"]


def load(
    obj: Any,
    loader_type: Type[Union[YAML_Loader, YAML_CLoader]],
    constructor: Constructor,
    inplace: bool = False,
    nested: bool = False,
) -> Any:
    """Recursively load and parse all :class:`.Data` instances inside ``obj``.

    If :attr:`.Constructor.autoload` is ``False``, :func:`yaml.load` will not cause including files to be opened or read,
    in the situation, what returned by :func:`yaml.load` is an object with :class:`.Data` in it, and the files won't be processed.
    Thus we use the function to open and parse those including files represented by :class:`.Data` instances inside `obj`.

    Args:
        obj: object containers :class:`.Data`
        loader_type: use this type of `PyYAML` Loader to parse string in including file(s)
        constructor: use this :class:`.Constructor` to find/open/read including file(s)
        inplace: whether to make a in-place replacement for every :class:`.Constructor` instance in ``obj``
        nested: whether to parse and load lower level include statement(s) inside :class:`.Constructor` instance

    Returns:
        Parsed object
    """
    if isinstance(obj, Data):
        d = constructor.load(loader_type, obj)
        if nested:
            return load(d, loader_type, constructor, inplace, nested)
        else:
            return d
    elif isinstance(obj, Mapping):
        if inplace:
            if not isinstance(obj, MutableMapping):
                raise ValueError(f"{obj} is not mutable")
            for k, v in obj.items():
                obj[k] = load(v, loader_type, constructor, inplace, nested)
        else:
            return {k: load(v, loader_type, constructor, inplace, nested) for k, v in obj.items()}
    elif isinstance(obj, Sequence) and not isinstance(obj, (bytearray, bytes, memoryview, str)):
        if inplace:
            if not isinstance(obj, MutableSequence):
                raise ValueError(f"{obj} is not mutable")
            for i, v in enumerate(obj):
                obj[i] = load(v, loader_type, constructor, inplace, nested)
        else:
            return [load(m, loader_type, constructor, inplace, nested) for m in obj]
    return obj


def lazy_load(
    obj: Any,
    loader_type: Type[Union[YAML_Loader, YAML_CLoader]],
    constructor: Constructor,
    nested: bool = False,
) -> Generator[Any, None, Any]:
    """Recursively load and parse all :class:`.Data` inside ``obj`` in generative mode.

    Almost the same as :func:`.load`, except that:

    * The function returns a :term:`generator`, it yields at every :class:`.Data` instance found in side ``obj``.
    * It only applies an in-place parsing and replacement, and will not return parsed object.
    """
    if isinstance(obj, Data):
        d = constructor.load(loader_type, obj)
        if nested:
            return (yield from lazy_load(d, loader_type, constructor, nested))
        else:
            return d
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = yield from lazy_load(v, loader_type, constructor, nested)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = yield from lazy_load(v, loader_type, constructor, nested)
    return obj
