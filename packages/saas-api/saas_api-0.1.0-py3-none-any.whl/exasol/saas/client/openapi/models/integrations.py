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
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="Integrations")


@_attrs_define
class Integrations:
    """ 
        Attributes:
            id (str):
            name (str):
            url (Union[Unset, str]):
     """

    id: str
    name: str
    url: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        url = self.url


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "id": id,
            "name": name,
        })
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        url = d.pop("url", UNSET)

        integrations = cls(
            id=id,
            name=name,
            url=url,
        )

        return integrations

