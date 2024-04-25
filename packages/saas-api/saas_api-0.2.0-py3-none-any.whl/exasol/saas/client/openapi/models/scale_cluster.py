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

T = TypeVar("T", bound="ScaleCluster")


@_attrs_define
class ScaleCluster:
    """ 
        Attributes:
            size (str):
     """

    size: str


    def to_dict(self) -> Dict[str, Any]:
        size = self.size


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "size": size,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size")

        scale_cluster = cls(
            size=size,
        )

        return scale_cluster

