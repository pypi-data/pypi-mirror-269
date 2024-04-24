from typing import Any, Iterator, Mapping, TypeVar, final

from attrs import frozen
from typing_extensions import Self
from wraps.wraps.option import wrap_option_on

__all__ = ("MappingView", "mapping_view")

K = TypeVar("K")
V = TypeVar("V")

wrap_key_error = wrap_option_on(KeyError)


@final
@frozen()
class MappingView(Mapping[K, V]):
    """Represents view over mappings."""

    mapping: Mapping[K, V]
    """The mapping to view."""

    def __iter__(self) -> Iterator[K]:
        yield from self.mapping

    def __getitem__(self, key: K) -> V:
        return self.mapping[key]

    def __contains__(self, key: Any) -> bool:
        return key in self.mapping

    def __len__(self) -> int:
        return len(self.mapping)

    @wrap_key_error
    def get_option(self, key: K) -> V:
        return self[key]

    def copy(self) -> Self:
        return type(self)(self)


def mapping_view(mapping: Mapping[K, V]) -> MappingView[K, V]:
    """Returns the [`MappingView[K, V]`][iters.mapping_view.MappingView] over the given mapping.

    Arguments:
        mapping: The mapping to view into.

    Returns:
        The view over the mapping.
    """
    return MappingView(mapping)
