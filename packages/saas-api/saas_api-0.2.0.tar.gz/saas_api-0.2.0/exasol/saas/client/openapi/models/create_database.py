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

if TYPE_CHECKING:
  from ..models.create_database_initial_cluster import CreateDatabaseInitialCluster





T = TypeVar("T", bound="CreateDatabase")


@_attrs_define
class CreateDatabase:
    """ 
        Attributes:
            name (str):
            initial_cluster (CreateDatabaseInitialCluster):
            provider (str):
            region (str):
     """

    name: str
    initial_cluster: 'CreateDatabaseInitialCluster'
    provider: str
    region: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_database_initial_cluster import (
            CreateDatabaseInitialCluster,
        )
        name = self.name

        initial_cluster = self.initial_cluster.to_dict()

        provider = self.provider

        region = self.region


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "initialCluster": initial_cluster,
            "provider": provider,
            "region": region,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_database_initial_cluster import (
            CreateDatabaseInitialCluster,
        )
        d = src_dict.copy()
        name = d.pop("name")

        initial_cluster = CreateDatabaseInitialCluster.from_dict(d.pop("initialCluster"))




        provider = d.pop("provider")

        region = d.pop("region")

        create_database = cls(
            name=name,
            initial_cluster=initial_cluster,
            provider=provider,
            region=region,
        )

        create_database.additional_properties = d
        return create_database

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
