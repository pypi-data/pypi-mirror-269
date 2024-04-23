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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import (
    UNSET,
    Unset,
)

if TYPE_CHECKING:
  from ..models.create_cluster import CreateCluster





T = TypeVar("T", bound="CreateDatabase")


@_attrs_define
class CreateDatabase:
    """ 
        Attributes:
            name (str):
            initial_cluster (CreateCluster):
            provider (str):
            region (str):
     """

    name: str
    initial_cluster: 'CreateCluster'
    provider: str
    region: str


    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_cluster import CreateCluster
        name = self.name

        initial_cluster = self.initial_cluster.to_dict()

        provider = self.provider

        region = self.region


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
            "initialCluster": initial_cluster,
            "provider": provider,
            "region": region,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_cluster import CreateCluster
        d = src_dict.copy()
        name = d.pop("name")

        initial_cluster = CreateCluster.from_dict(d.pop("initialCluster"))




        provider = d.pop("provider")

        region = d.pop("region")

        create_database = cls(
            name=name,
            initial_cluster=initial_cluster,
            provider=provider,
            region=region,
        )

        return create_database

