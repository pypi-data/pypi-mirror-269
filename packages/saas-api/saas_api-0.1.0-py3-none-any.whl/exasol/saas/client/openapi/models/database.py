import datetime
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
  from ..models.cluster_overview import ClusterOverview
  from ..models.integrations import Integrations





T = TypeVar("T", bound="Database")


@_attrs_define
class Database:
    """ 
        Attributes:
            status (Status):
            id (str):
            name (str):
            clusters (ClusterOverview):
            provider (str):
            region (str):
            created_at (datetime.datetime):
            created_by (str):
            integrations (Union[Unset, List['Integrations']]):
            deleted_by (Union[Unset, str]):
            deleted_at (Union[Unset, datetime.datetime]):
     """

    status: Status
    id: str
    name: str
    clusters: 'ClusterOverview'
    provider: str
    region: str
    created_at: datetime.datetime
    created_by: str
    integrations: Union[Unset, List['Integrations']] = UNSET
    deleted_by: Union[Unset, str] = UNSET
    deleted_at: Union[Unset, datetime.datetime] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        from ..models.cluster_overview import ClusterOverview
        from ..models.integrations import Integrations
        status = self.status.value

        id = self.id

        name = self.name

        clusters = self.clusters.to_dict()

        provider = self.provider

        region = self.region

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        integrations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.integrations, Unset):
            integrations = []
            for integrations_item_data in self.integrations:
                integrations_item = integrations_item_data.to_dict()
                integrations.append(integrations_item)





        deleted_by = self.deleted_by

        deleted_at: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "status": status,
            "id": id,
            "name": name,
            "clusters": clusters,
            "provider": provider,
            "region": region,
            "createdAt": created_at,
            "createdBy": created_by,
        })
        if integrations is not UNSET:
            field_dict["integrations"] = integrations
        if deleted_by is not UNSET:
            field_dict["deletedBy"] = deleted_by
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cluster_overview import ClusterOverview
        from ..models.integrations import Integrations
        d = src_dict.copy()
        status = Status(d.pop("status"))




        id = d.pop("id")

        name = d.pop("name")

        clusters = ClusterOverview.from_dict(d.pop("clusters"))




        provider = d.pop("provider")

        region = d.pop("region")

        created_at = isoparse(d.pop("createdAt"))




        created_by = d.pop("createdBy")

        integrations = []
        _integrations = d.pop("integrations", UNSET)
        for integrations_item_data in (_integrations or []):
            integrations_item = Integrations.from_dict(integrations_item_data)



            integrations.append(integrations_item)


        deleted_by = d.pop("deletedBy", UNSET)

        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: Union[Unset, datetime.datetime]
        if isinstance(_deleted_at,  Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)




        database = cls(
            status=status,
            id=id,
            name=name,
            clusters=clusters,
            provider=provider,
            region=region,
            created_at=created_at,
            created_by=created_by,
            integrations=integrations,
            deleted_by=deleted_by,
            deleted_at=deleted_at,
        )

        return database

