import datetime
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
from dateutil.parser import isoparse

from ..models.status import Status
from ..types import (
    UNSET,
    Unset,
)

if TYPE_CHECKING:
  from ..models.auto_stop import AutoStop





T = TypeVar("T", bound="Cluster")


@_attrs_define
class Cluster:
    """ 
        Attributes:
            status (Status):
            id (str):
            name (str):
            size (str):
            created_at (datetime.datetime):
            created_by (str):
            main_cluster (bool):
            deleted_at (Union[Unset, datetime.datetime]):
            deleted_by (Union[Unset, str]):
            auto_stop (Union[Unset, AutoStop]):
     """

    status: Status
    id: str
    name: str
    size: str
    created_at: datetime.datetime
    created_by: str
    main_cluster: bool
    deleted_at: Union[Unset, datetime.datetime] = UNSET
    deleted_by: Union[Unset, str] = UNSET
    auto_stop: Union[Unset, 'AutoStop'] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        from ..models.auto_stop import AutoStop
        status = self.status.value

        id = self.id

        name = self.name

        size = self.size

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        main_cluster = self.main_cluster

        deleted_at: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()

        deleted_by = self.deleted_by

        auto_stop: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auto_stop, Unset):
            auto_stop = self.auto_stop.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "status": status,
            "id": id,
            "name": name,
            "size": size,
            "createdAt": created_at,
            "createdBy": created_by,
            "mainCluster": main_cluster,
        })
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at
        if deleted_by is not UNSET:
            field_dict["deletedBy"] = deleted_by
        if auto_stop is not UNSET:
            field_dict["autoStop"] = auto_stop

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.auto_stop import AutoStop
        d = src_dict.copy()
        status = Status(d.pop("status"))




        id = d.pop("id")

        name = d.pop("name")

        size = d.pop("size")

        created_at = isoparse(d.pop("createdAt"))




        created_by = d.pop("createdBy")

        main_cluster = d.pop("mainCluster")

        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: Union[Unset, datetime.datetime]
        if isinstance(_deleted_at,  Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)




        deleted_by = d.pop("deletedBy", UNSET)

        _auto_stop = d.pop("autoStop", UNSET)
        auto_stop: Union[Unset, AutoStop]
        if isinstance(_auto_stop,  Unset):
            auto_stop = UNSET
        else:
            auto_stop = AutoStop.from_dict(_auto_stop)




        cluster = cls(
            status=status,
            id=id,
            name=name,
            size=size,
            created_at=created_at,
            created_by=created_by,
            main_cluster=main_cluster,
            deleted_at=deleted_at,
            deleted_by=deleted_by,
            auto_stop=auto_stop,
        )

        return cluster

