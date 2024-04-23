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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="APIErrorCauses")


@_attrs_define
class APIErrorCauses:
    """ 
     """

    additional_properties: Dict[str, bool] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_error_causes = cls(
        )


        api_error_causes.additional_properties = d
        return api_error_causes

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> bool:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: bool) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
