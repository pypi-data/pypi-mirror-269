from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    List,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="PatchUserDatabases")


@_attrs_define
class PatchUserDatabases:
    """ 
        Attributes:
            delete (List[str]):
            add (List[str]):
     """

    delete: List[str]
    add: List[str]


    def to_dict(self) -> Dict[str, Any]:
        delete = self.delete





        add = self.add






        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "delete": delete,
            "add": add,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        delete = cast(List[str], d.pop("delete"))


        add = cast(List[str], d.pop("add"))


        patch_user_databases = cls(
            delete=delete,
            add=add,
        )

        return patch_user_databases

