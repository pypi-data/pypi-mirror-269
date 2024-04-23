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

T = TypeVar("T", bound="UpdateDatabase")


@_attrs_define
class UpdateDatabase:
    """ 
        Attributes:
            name (str):
     """

    name: str


    def to_dict(self) -> Dict[str, Any]:
        name = self.name


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        update_database = cls(
            name=name,
        )

        return update_database

