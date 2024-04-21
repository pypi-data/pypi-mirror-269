from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Literal, Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="CheckInviteResponse")


@_attrs_define
class CheckInviteResponse:
    """
    Attributes:
        status (int):
        location (str):
        type (Union[Literal['urn:invariant:responses:check_invite_response'], Unset]):  Default:
            'urn:invariant:responses:check_invite_response'.
    """

    status: int
    location: str
    type: Union[
        Literal["urn:invariant:responses:check_invite_response"], Unset
    ] = "urn:invariant:responses:check_invite_response"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        location = self.location
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "location": location,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        location = d.pop("location")

        type = d.pop("type", UNSET)

        check_invite_response = cls(
            status=status,
            location=location,
            type=type,
        )

        check_invite_response.additional_properties = d
        return check_invite_response

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
