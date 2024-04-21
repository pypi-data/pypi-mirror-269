from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.validation_error_response import ValidationErrorResponse
from ...models.check_invite_response import CheckInviteResponse
from typing import Dict
from ...models.challenge_response import ChallengeResponse
from ...models.base_error_response import BaseErrorResponse


def _get_kwargs() -> Dict[str, Any]:
    return {
        "method": "post",
        "url": "/api/v1/login/check_invite",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        CheckInviteResponse,
        ValidationErrorResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CheckInviteResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = BaseErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = BaseErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        CheckInviteResponse,
        ValidationErrorResponse,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        CheckInviteResponse,
        ValidationErrorResponse,
    ]
]:
    """Consume an email invitation magic link

     Consume an email invitation magic link.

    If the email is already associated with an active login, this will
    link the new user and active login and issue an HTTPOnly refresh token cookie.

    Otherwise, a ChallengeResponse will be issued with next=new_password.

    This function can also handle the case where the login was created with a pre-set password,
    although creating such a login may not be supported.

    This function also marks the linked login as email_validated=True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseErrorResponse, ChallengeResponse, CheckInviteResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        CheckInviteResponse,
        ValidationErrorResponse,
    ]
]:
    """Consume an email invitation magic link

     Consume an email invitation magic link.

    If the email is already associated with an active login, this will
    link the new user and active login and issue an HTTPOnly refresh token cookie.

    Otherwise, a ChallengeResponse will be issued with next=new_password.

    This function can also handle the case where the login was created with a pre-set password,
    although creating such a login may not be supported.

    This function also marks the linked login as email_validated=True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseErrorResponse, ChallengeResponse, CheckInviteResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        CheckInviteResponse,
        ValidationErrorResponse,
    ]
]:
    """Consume an email invitation magic link

     Consume an email invitation magic link.

    If the email is already associated with an active login, this will
    link the new user and active login and issue an HTTPOnly refresh token cookie.

    Otherwise, a ChallengeResponse will be issued with next=new_password.

    This function can also handle the case where the login was created with a pre-set password,
    although creating such a login may not be supported.

    This function also marks the linked login as email_validated=True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseErrorResponse, ChallengeResponse, CheckInviteResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        CheckInviteResponse,
        ValidationErrorResponse,
    ]
]:
    """Consume an email invitation magic link

     Consume an email invitation magic link.

    If the email is already associated with an active login, this will
    link the new user and active login and issue an HTTPOnly refresh token cookie.

    Otherwise, a ChallengeResponse will be issued with next=new_password.

    This function can also handle the case where the login was created with a pre-set password,
    although creating such a login may not be supported.

    This function also marks the linked login as email_validated=True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseErrorResponse, ChallengeResponse, CheckInviteResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
