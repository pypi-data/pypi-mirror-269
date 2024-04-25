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

T = TypeVar("T", bound="ExtensionParameterDefinitions")


@_attrs_define
class ExtensionParameterDefinitions:
    """ 
        Attributes:
            id (str):
            name (str):
            raw_definition (Union[Unset, Any]):
     """

    id: str
    name: str
    raw_definition: Union[Unset, Any] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        raw_definition = self.raw_definition


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "id": id,
            "name": name,
        })
        if raw_definition is not UNSET:
            field_dict["rawDefinition"] = raw_definition

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        raw_definition = d.pop("rawDefinition", UNSET)

        extension_parameter_definitions = cls(
            id=id,
            name=name,
            raw_definition=raw_definition,
        )

        return extension_parameter_definitions

