from dataclasses import dataclass, replace
from typing import Tuple, TypeVar

from ..common import TypeHint
from ..datastructures import ImmutableStack
from ..definitions import DebugTrail
from ..type_tools import BaseNormType, normalize_type
from ..utils import pairs
from .essential import CannotProvide, Request
from .location import AnyLoc, FieldLoc, TypeHintLoc

LocStackT = TypeVar("LocStackT", bound="LocStack")
AnyLocT_co = TypeVar("AnyLocT_co", bound=AnyLoc, covariant=True)


class LocStack(ImmutableStack[AnyLocT_co]):
    def replace_last_type(self: LocStackT, tp: TypeHint, /) -> LocStackT:
        return self.replace_last(replace(self.last, type=tp))


T = TypeVar("T")


@dataclass(frozen=True)
class LocatedRequest(Request[T]):
    loc_stack: LocStack

    @property
    def last_loc(self) -> AnyLoc:
        return self.loc_stack.last


def get_type_from_request(request: LocatedRequest) -> TypeHint:
    return request.last_loc.cast_or_raise(TypeHintLoc, CannotProvide).type


def try_normalize_type(tp: TypeHint) -> BaseNormType:
    try:
        return normalize_type(tp)
    except ValueError:
        raise CannotProvide(f"{tp} can not be normalized")


class StrictCoercionRequest(LocatedRequest[bool]):
    pass


class DebugTrailRequest(LocatedRequest[DebugTrail]):
    pass


def find_owner_with_field(stack: LocStack) -> Tuple[TypeHintLoc, FieldLoc]:
    for next_loc, prev_loc in pairs(reversed(stack)):
        if next_loc.is_castable(FieldLoc):
            return prev_loc, next_loc
    raise ValueError
