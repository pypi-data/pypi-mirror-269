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

from ..types import (
    UNSET,
    Unset,
)

T = TypeVar("T", bound="File")


@_attrs_define
class File:
    """ 
        Attributes:
            name (str):
            type (str):
            path (str):
            last_modified (datetime.datetime):
            size (Union[Unset, int]):
            children (Union[Unset, List['File']]):
     """

    name: str
    type: str
    path: str
    last_modified: datetime.datetime
    size: Union[Unset, int] = UNSET
    children: Union[Unset, List['File']] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        type = self.type

        path = self.path

        last_modified = self.last_modified.isoformat()

        size = self.size

        children: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)






        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
            "type": type,
            "path": path,
            "lastModified": last_modified,
        })
        if size is not UNSET:
            field_dict["size"] = size
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = d.pop("type")

        path = d.pop("path")

        last_modified = isoparse(d.pop("lastModified"))




        size = d.pop("size", UNSET)

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in (_children or []):
            children_item = File.from_dict(children_item_data)



            children.append(children_item)


        file = cls(
            name=name,
            type=type,
            path=path,
            last_modified=last_modified,
            size=size,
            children=children,
        )

        return file

