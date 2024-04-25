from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="DatabaseClusters")


@_attrs_define
class DatabaseClusters:
    """ 
        Attributes:
            total (int):
            running (int):
     """

    total: int
    running: int


    def to_dict(self) -> Dict[str, Any]:
        total = self.total

        running = self.running


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "total": total,
            "running": running,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total = d.pop("total")

        running = d.pop("running")

        database_clusters = cls(
            total=total,
            running=running,
        )

        return database_clusters

