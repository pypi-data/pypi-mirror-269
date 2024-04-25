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

from ..types import (
    UNSET,
    Unset,
)

if TYPE_CHECKING:
  from ..models.usage_cluster import UsageCluster





T = TypeVar("T", bound="UsageAdditionalPropertyItem")


@_attrs_define
class UsageAdditionalPropertyItem:
    """ 
        Attributes:
            id (str):
            name (str):
            clusters (List['UsageCluster']):
            used_storage (Union[Unset, float]):
     """

    id: str
    name: str
    clusters: List['UsageCluster']
    used_storage: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        from ..models.usage_cluster import UsageCluster
        id = self.id

        name = self.name

        clusters = []
        for clusters_item_data in self.clusters:
            clusters_item = clusters_item_data.to_dict()
            clusters.append(clusters_item)





        used_storage = self.used_storage


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "id": id,
            "name": name,
            "clusters": clusters,
        })
        if used_storage is not UNSET:
            field_dict["usedStorage"] = used_storage

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.usage_cluster import UsageCluster
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        clusters = []
        _clusters = d.pop("clusters")
        for clusters_item_data in (_clusters):
            clusters_item = UsageCluster.from_dict(clusters_item_data)



            clusters.append(clusters_item)


        used_storage = d.pop("usedStorage", UNSET)

        usage_additional_property_item = cls(
            id=id,
            name=name,
            clusters=clusters,
            used_storage=used_storage,
        )

        return usage_additional_property_item

