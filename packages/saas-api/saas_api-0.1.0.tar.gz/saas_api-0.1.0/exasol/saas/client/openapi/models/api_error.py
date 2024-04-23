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

from ..types import (
    UNSET,
    Unset,
)

if TYPE_CHECKING:
  from ..models.api_error_causes import APIErrorCauses





T = TypeVar("T", bound="APIError")


@_attrs_define
class APIError:
    """ 
        Attributes:
            code (int):
            message (str):
            causes (Union[Unset, APIErrorCauses]):
            request_id (Union[Unset, str]):
            timestamp (Union[Unset, datetime.datetime]):
            api_id (Union[Unset, str]):
     """

    code: int
    message: str
    causes: Union[Unset, 'APIErrorCauses'] = UNSET
    request_id: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    api_id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        from ..models.api_error_causes import APIErrorCauses
        code = self.code

        message = self.message

        causes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.causes, Unset):
            causes = self.causes.to_dict()

        request_id = self.request_id

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        api_id = self.api_id


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "code": code,
            "message": message,
        })
        if causes is not UNSET:
            field_dict["causes"] = causes
        if request_id is not UNSET:
            field_dict["requestID"] = request_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if api_id is not UNSET:
            field_dict["apiID"] = api_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_error_causes import APIErrorCauses
        d = src_dict.copy()
        code = d.pop("code")

        message = d.pop("message")

        _causes = d.pop("causes", UNSET)
        causes: Union[Unset, APIErrorCauses]
        if isinstance(_causes,  Unset):
            causes = UNSET
        else:
            causes = APIErrorCauses.from_dict(_causes)




        request_id = d.pop("requestID", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp,  Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)




        api_id = d.pop("apiID", UNSET)

        api_error = cls(
            code=code,
            message=message,
            causes=causes,
            request_id=request_id,
            timestamp=timestamp,
            api_id=api_id,
        )

        return api_error

