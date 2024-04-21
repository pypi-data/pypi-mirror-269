from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.validation_error_response import ValidationErrorResponse
from typing import Dict
from ...models.login_request import LoginRequest
from typing import cast
from ...models.base_error_response import BaseErrorResponse
from ...models.challenge_response import ChallengeResponse


def _get_kwargs(
    *,
    json_body: LoginRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/login/",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
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
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
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
    json_body: LoginRequest,
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Authenticate and respond to authentication challenges

     To authenticate, send a request with basic_auth provided.

    If additional steps are neded by the user, this API will send a ChallengeResponse (HTTP 401),
    which includes a challenge type and a Login Session Token. Use this API to respond to the challenge
    and send the given token.

    On successful authentication an HTTPOnly refresh token cookie will be issued through a set-cookie
    header.

    Note: this is not the only authentication entrypoint. It is also possible to authenticate from a
    single-use email invitation link using the /check_invite method.

    ## Using the cookie

    The HTTPOnly refresh token cookie can be used to:

    -   Get a list of available instances: /get_instances.
    -   Get an instance access token: /:org/api/v1/refresh.
    -   Refresh the refresh token before it expires: /refresh.

    ## Basic authentication

        Key: basic_auth
        Authentication: none

    Provide an email and password value. If the password is incorrect a ChallengeResponse will be issued
    with
    challenge=basic_auth.

    ## Email verification

        Key: email_valid
        Authentication: Login Session Token

    Provide a secret PIN value from the verification email. The PIN must be non-expired and is consumed
    on use.
    /resend_validation_pin can be used to re-send a verification email.

    ## Password reset

        Key: reset_request
        Authentication: none

    Provide an email to send a password reset email to it. A ChallengeResponse will be issued with
    challenge=reset_pin .

    ## Password reset check PIN

        Key: reset_pin_request
        Authentication: Login Session Token

    Provide a secret PIN value from the password reset email. The PIN must be non-expired. Checking the
    PIN
    does not consume it, it will be re-checked and consumed when the user provides a new password. A
    ChallengeResponse will be issued with challenge=new_password .

    ## New password

        Key: new_password
        Authentication: Login Session Token

    Provide a new password and a secret PIN value from the password reset email OR an email invitation
    token (which is a JWT
    containing a secret PIN). The PIN must be non-expired and will be consumed on use.

    Args:
        json_body (LoginRequest): Request to determine login method (Basic, SAML, etc).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: LoginRequest,
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Authenticate and respond to authentication challenges

     To authenticate, send a request with basic_auth provided.

    If additional steps are neded by the user, this API will send a ChallengeResponse (HTTP 401),
    which includes a challenge type and a Login Session Token. Use this API to respond to the challenge
    and send the given token.

    On successful authentication an HTTPOnly refresh token cookie will be issued through a set-cookie
    header.

    Note: this is not the only authentication entrypoint. It is also possible to authenticate from a
    single-use email invitation link using the /check_invite method.

    ## Using the cookie

    The HTTPOnly refresh token cookie can be used to:

    -   Get a list of available instances: /get_instances.
    -   Get an instance access token: /:org/api/v1/refresh.
    -   Refresh the refresh token before it expires: /refresh.

    ## Basic authentication

        Key: basic_auth
        Authentication: none

    Provide an email and password value. If the password is incorrect a ChallengeResponse will be issued
    with
    challenge=basic_auth.

    ## Email verification

        Key: email_valid
        Authentication: Login Session Token

    Provide a secret PIN value from the verification email. The PIN must be non-expired and is consumed
    on use.
    /resend_validation_pin can be used to re-send a verification email.

    ## Password reset

        Key: reset_request
        Authentication: none

    Provide an email to send a password reset email to it. A ChallengeResponse will be issued with
    challenge=reset_pin .

    ## Password reset check PIN

        Key: reset_pin_request
        Authentication: Login Session Token

    Provide a secret PIN value from the password reset email. The PIN must be non-expired. Checking the
    PIN
    does not consume it, it will be re-checked and consumed when the user provides a new password. A
    ChallengeResponse will be issued with challenge=new_password .

    ## New password

        Key: new_password
        Authentication: Login Session Token

    Provide a new password and a secret PIN value from the password reset email OR an email invitation
    token (which is a JWT
    containing a secret PIN). The PIN must be non-expired and will be consumed on use.

    Args:
        json_body (LoginRequest): Request to determine login method (Basic, SAML, etc).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: LoginRequest,
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Authenticate and respond to authentication challenges

     To authenticate, send a request with basic_auth provided.

    If additional steps are neded by the user, this API will send a ChallengeResponse (HTTP 401),
    which includes a challenge type and a Login Session Token. Use this API to respond to the challenge
    and send the given token.

    On successful authentication an HTTPOnly refresh token cookie will be issued through a set-cookie
    header.

    Note: this is not the only authentication entrypoint. It is also possible to authenticate from a
    single-use email invitation link using the /check_invite method.

    ## Using the cookie

    The HTTPOnly refresh token cookie can be used to:

    -   Get a list of available instances: /get_instances.
    -   Get an instance access token: /:org/api/v1/refresh.
    -   Refresh the refresh token before it expires: /refresh.

    ## Basic authentication

        Key: basic_auth
        Authentication: none

    Provide an email and password value. If the password is incorrect a ChallengeResponse will be issued
    with
    challenge=basic_auth.

    ## Email verification

        Key: email_valid
        Authentication: Login Session Token

    Provide a secret PIN value from the verification email. The PIN must be non-expired and is consumed
    on use.
    /resend_validation_pin can be used to re-send a verification email.

    ## Password reset

        Key: reset_request
        Authentication: none

    Provide an email to send a password reset email to it. A ChallengeResponse will be issued with
    challenge=reset_pin .

    ## Password reset check PIN

        Key: reset_pin_request
        Authentication: Login Session Token

    Provide a secret PIN value from the password reset email. The PIN must be non-expired. Checking the
    PIN
    does not consume it, it will be re-checked and consumed when the user provides a new password. A
    ChallengeResponse will be issued with challenge=new_password .

    ## New password

        Key: new_password
        Authentication: Login Session Token

    Provide a new password and a secret PIN value from the password reset email OR an email invitation
    token (which is a JWT
    containing a secret PIN). The PIN must be non-expired and will be consumed on use.

    Args:
        json_body (LoginRequest): Request to determine login method (Basic, SAML, etc).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: LoginRequest,
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Authenticate and respond to authentication challenges

     To authenticate, send a request with basic_auth provided.

    If additional steps are neded by the user, this API will send a ChallengeResponse (HTTP 401),
    which includes a challenge type and a Login Session Token. Use this API to respond to the challenge
    and send the given token.

    On successful authentication an HTTPOnly refresh token cookie will be issued through a set-cookie
    header.

    Note: this is not the only authentication entrypoint. It is also possible to authenticate from a
    single-use email invitation link using the /check_invite method.

    ## Using the cookie

    The HTTPOnly refresh token cookie can be used to:

    -   Get a list of available instances: /get_instances.
    -   Get an instance access token: /:org/api/v1/refresh.
    -   Refresh the refresh token before it expires: /refresh.

    ## Basic authentication

        Key: basic_auth
        Authentication: none

    Provide an email and password value. If the password is incorrect a ChallengeResponse will be issued
    with
    challenge=basic_auth.

    ## Email verification

        Key: email_valid
        Authentication: Login Session Token

    Provide a secret PIN value from the verification email. The PIN must be non-expired and is consumed
    on use.
    /resend_validation_pin can be used to re-send a verification email.

    ## Password reset

        Key: reset_request
        Authentication: none

    Provide an email to send a password reset email to it. A ChallengeResponse will be issued with
    challenge=reset_pin .

    ## Password reset check PIN

        Key: reset_pin_request
        Authentication: Login Session Token

    Provide a secret PIN value from the password reset email. The PIN must be non-expired. Checking the
    PIN
    does not consume it, it will be re-checked and consumed when the user provides a new password. A
    ChallengeResponse will be issued with challenge=new_password .

    ## New password

        Key: new_password
        Authentication: Login Session Token

    Provide a new password and a secret PIN value from the password reset email OR an email invitation
    token (which is a JWT
    containing a secret PIN). The PIN must be non-expired and will be consumed on use.

    Args:
        json_body (LoginRequest): Request to determine login method (Basic, SAML, etc).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
