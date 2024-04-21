from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict

if TYPE_CHECKING:
    from ..models.login import Login
    from ..models.organization import Organization


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        uuid (str):
        organization (Organization):
        login (Login):
        email (str):
        is_active (bool):
        is_superuser (bool):
    """

    uuid: str
    organization: "Organization"
    login: "Login"
    email: str
    is_active: bool
    is_superuser: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        organization = self.organization.to_dict()

        login = self.login.to_dict()

        email = self.email
        is_active = self.is_active
        is_superuser = self.is_superuser

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "organization": organization,
                "login": login,
                "email": email,
                "is_active": is_active,
                "is_superuser": is_superuser,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.login import Login
        from ..models.organization import Organization

        d = src_dict.copy()
        uuid = d.pop("uuid")

        organization = Organization.from_dict(d.pop("organization"))

        login = Login.from_dict(d.pop("login"))

        email = d.pop("email")

        is_active = d.pop("is_active")

        is_superuser = d.pop("is_superuser")

        user = cls(
            uuid=uuid,
            organization=organization,
            login=login,
            email=email,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        user.additional_properties = d
        return user

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
