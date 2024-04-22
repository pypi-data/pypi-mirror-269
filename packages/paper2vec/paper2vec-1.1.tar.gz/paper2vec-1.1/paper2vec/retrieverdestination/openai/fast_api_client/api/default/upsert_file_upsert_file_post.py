from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.upsert_response import UpsertResponse
from ...models.body_upsert_file_upsert_file_post import BodyUpsertFileUpsertFilePost
from typing import Dict
from typing import cast
from ...models.http_validation_error import HTTPValidationError



def _get_kwargs(
    *,
    body: BodyUpsertFileUpsertFilePost,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/upsert-file",
    }

    _body = body.to_multipart()



    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[HTTPValidationError, UpsertResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpsertResponse.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[HTTPValidationError, UpsertResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyUpsertFileUpsertFilePost,

) -> Response[Union[HTTPValidationError, UpsertResponse]]:
    """ Upsert File

    Args:
        body (BodyUpsertFileUpsertFilePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UpsertResponse]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: BodyUpsertFileUpsertFilePost,

) -> Optional[Union[HTTPValidationError, UpsertResponse]]:
    """ Upsert File

    Args:
        body (BodyUpsertFileUpsertFilePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UpsertResponse]
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyUpsertFileUpsertFilePost,

) -> Response[Union[HTTPValidationError, UpsertResponse]]:
    """ Upsert File

    Args:
        body (BodyUpsertFileUpsertFilePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UpsertResponse]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BodyUpsertFileUpsertFilePost,

) -> Optional[Union[HTTPValidationError, UpsertResponse]]:
    """ Upsert File

    Args:
        body (BodyUpsertFileUpsertFilePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UpsertResponse]
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
