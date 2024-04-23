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

T = TypeVar("T", bound="DownloadFile")


@_attrs_define
class DownloadFile:
    """ 
        Attributes:
            url (str):
     """

    url: str


    def to_dict(self) -> Dict[str, Any]:
        url = self.url


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "url": url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        download_file = cls(
            url=url,
        )

        return download_file

