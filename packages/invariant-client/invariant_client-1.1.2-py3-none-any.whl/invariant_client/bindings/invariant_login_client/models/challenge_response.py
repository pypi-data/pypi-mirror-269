from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import Literal
from ..types import UNSET, Unset
from ..models.challenge_response_challenge import ChallengeResponseChallenge
from typing import cast, Union


T = TypeVar("T", bound="ChallengeResponse")


@_attrs_define
class ChallengeResponse:
    """
    Attributes:
        status (int):
        type (Literal['urn:invariant:errors:auth_challenge']):
        title (str):
        detail (str):
        challenge (ChallengeResponseChallenge):
        instance (Union[None, Unset, str]):
        login_token (Union[None, Unset, str]):
    """

    status: int
    type: Literal["urn:invariant:errors:auth_challenge"]
    title: str
    detail: str
    challenge: ChallengeResponseChallenge
    instance: Union[None, Unset, str] = UNSET
    login_token: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        type = self.type
        title = self.title
        detail = self.detail
        challenge = self.challenge.value

        instance: Union[None, Unset, str]
        if isinstance(self.instance, Unset):
            instance = UNSET

        else:
            instance = self.instance

        login_token: Union[None, Unset, str]
        if isinstance(self.login_token, Unset):
            login_token = UNSET

        else:
            login_token = self.login_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "type": type,
                "title": title,
                "detail": detail,
                "challenge": challenge,
            }
        )
        if instance is not UNSET:
            field_dict["instance"] = instance
        if login_token is not UNSET:
            field_dict["login_token"] = login_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        type = d.pop("type")

        title = d.pop("title")

        detail = d.pop("detail")

        challenge = ChallengeResponseChallenge(d.pop("challenge"))

        def _parse_instance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instance = _parse_instance(d.pop("instance", UNSET))

        def _parse_login_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        login_token = _parse_login_token(d.pop("login_token", UNSET))

        challenge_response = cls(
            status=status,
            type=type,
            title=title,
            detail=detail,
            challenge=challenge,
            instance=instance,
            login_token=login_token,
        )

        challenge_response.additional_properties = d
        return challenge_response

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
