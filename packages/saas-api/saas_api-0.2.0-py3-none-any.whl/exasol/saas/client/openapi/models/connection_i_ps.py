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

T = TypeVar("T", bound="ConnectionIPs")


@_attrs_define
class ConnectionIPs:
    """ 
        Attributes:
            private (List[str]):
            public (List[str]):
     """

    private: List[str]
    public: List[str]


    def to_dict(self) -> Dict[str, Any]:
        private = self.private





        public = self.public






        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "private": private,
            "public": public,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        private = cast(List[str], d.pop("private"))


        public = cast(List[str], d.pop("public"))


        connection_i_ps = cls(
            private=private,
            public=public,
        )

        return connection_i_ps

