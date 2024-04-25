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

T = TypeVar("T", bound="ExtensionInstance")


@_attrs_define
class ExtensionInstance:
    """ 
        Attributes:
            id (str):
            name (str):
     """

    id: str
    name: str


    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "id": id,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        extension_instance = cls(
            id=id,
            name=name,
        )

        return extension_instance

