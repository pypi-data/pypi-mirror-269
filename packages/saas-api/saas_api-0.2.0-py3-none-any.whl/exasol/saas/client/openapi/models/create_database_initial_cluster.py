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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

if TYPE_CHECKING:
  from ..models.auto_stop import AutoStop





T = TypeVar("T", bound="CreateDatabaseInitialCluster")


@_attrs_define
class CreateDatabaseInitialCluster:
    """ 
        Attributes:
            name (str):
            size (str):
            auto_stop (Union[Unset, AutoStop]):
     """

    name: str
    size: str
    auto_stop: Union[Unset, 'AutoStop'] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        from ..models.auto_stop import AutoStop
        name = self.name

        size = self.size

        auto_stop: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auto_stop, Unset):
            auto_stop = self.auto_stop.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
            "size": size,
        })
        if auto_stop is not UNSET:
            field_dict["autoStop"] = auto_stop

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.auto_stop import AutoStop
        d = src_dict.copy()
        name = d.pop("name")

        size = d.pop("size")

        _auto_stop = d.pop("autoStop", UNSET)
        auto_stop: Union[Unset, AutoStop]
        if isinstance(_auto_stop,  Unset):
            auto_stop = UNSET
        else:
            auto_stop = AutoStop.from_dict(_auto_stop)




        create_database_initial_cluster = cls(
            name=name,
            size=size,
            auto_stop=auto_stop,
        )

        return create_database_initial_cluster

