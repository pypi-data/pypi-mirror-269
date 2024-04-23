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

T = TypeVar("T", bound="UpdateAllowedIP")


@_attrs_define
class UpdateAllowedIP:
    """ 
        Attributes:
            name (str):
            cidr_ip (str):
     """

    name: str
    cidr_ip: str


    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        cidr_ip = self.cidr_ip


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
            "cidrIp": cidr_ip,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        cidr_ip = d.pop("cidrIp")

        update_allowed_ip = cls(
            name=name,
            cidr_ip=cidr_ip,
        )

        return update_allowed_ip

