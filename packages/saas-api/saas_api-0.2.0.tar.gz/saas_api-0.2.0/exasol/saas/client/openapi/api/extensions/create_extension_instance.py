from http import HTTPStatus
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    cast,
)

import httpx

from ... import errors
from ...client import (
    AuthenticatedClient,
    Client,
)
from ...models.create_extension_instance import CreateExtensionInstance
from ...models.extension_instance import ExtensionInstance
from ...types import (
    UNSET,
    Response,
)


def _get_kwargs(
    account_id: str,
    database_id: str,
    extension_id: str,
    extension_version: str,
    *,
    body: CreateExtensionInstance,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/accounts/{account_id}/databases/{database_id}/extensions/{extension_id}/{extension_version}/instances".format(account_id=account_id,database_id=database_id,extension_id=extension_id,extension_version=extension_version,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ExtensionInstance]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExtensionInstance.from_dict(response.json())



        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ExtensionInstance]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    database_id: str,
    extension_id: str,
    extension_version: str,
    *,
    client: AuthenticatedClient,
    body: CreateExtensionInstance,

) -> Response[ExtensionInstance]:
    """ 
    Args:
        account_id (str):
        database_id (str):
        extension_id (str):
        extension_version (str):
        body (CreateExtensionInstance):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExtensionInstance]
     """


    kwargs = _get_kwargs(
        account_id=account_id,
database_id=database_id,
extension_id=extension_id,
extension_version=extension_version,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    account_id: str,
    database_id: str,
    extension_id: str,
    extension_version: str,
    *,
    client: AuthenticatedClient,
    body: CreateExtensionInstance,

) -> Optional[ExtensionInstance]:
    """ 
    Args:
        account_id (str):
        database_id (str):
        extension_id (str):
        extension_version (str):
        body (CreateExtensionInstance):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExtensionInstance
     """


    return sync_detailed(
        account_id=account_id,
database_id=database_id,
extension_id=extension_id,
extension_version=extension_version,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    account_id: str,
    database_id: str,
    extension_id: str,
    extension_version: str,
    *,
    client: AuthenticatedClient,
    body: CreateExtensionInstance,

) -> Response[ExtensionInstance]:
    """ 
    Args:
        account_id (str):
        database_id (str):
        extension_id (str):
        extension_version (str):
        body (CreateExtensionInstance):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExtensionInstance]
     """


    kwargs = _get_kwargs(
        account_id=account_id,
database_id=database_id,
extension_id=extension_id,
extension_version=extension_version,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    account_id: str,
    database_id: str,
    extension_id: str,
    extension_version: str,
    *,
    client: AuthenticatedClient,
    body: CreateExtensionInstance,

) -> Optional[ExtensionInstance]:
    """ 
    Args:
        account_id (str):
        database_id (str):
        extension_id (str):
        extension_version (str):
        body (CreateExtensionInstance):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExtensionInstance
     """


    return (await asyncio_detailed(
        account_id=account_id,
database_id=database_id,
extension_id=extension_id,
extension_version=extension_version,
client=client,
body=body,

    )).parsed
