from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Dict
from typing import cast
from typing import Union
from typing import cast, Union

if TYPE_CHECKING:
    from ..models.email_password_login import EmailPasswordLogin
    from ..models.reset_pin_request import ResetPINRequest
    from ..models.reset_request import ResetRequest
    from ..models.validation_request import ValidationRequest
    from ..models.new_password_request import NewPasswordRequest


T = TypeVar("T", bound="LoginRequest")


@_attrs_define
class LoginRequest:
    """Request to determine login method (Basic, SAML, etc).

    Attributes:
        basic_auth (Union['EmailPasswordLogin', None, Unset]):
        email_valid (Union['ValidationRequest', None, Unset]):
        reset_request (Union['ResetRequest', None, Unset]):
        reset_pin_request (Union['ResetPINRequest', None, Unset]):
        new_password (Union['NewPasswordRequest', None, Unset]):
    """

    basic_auth: Union["EmailPasswordLogin", None, Unset] = UNSET
    email_valid: Union["ValidationRequest", None, Unset] = UNSET
    reset_request: Union["ResetRequest", None, Unset] = UNSET
    reset_pin_request: Union["ResetPINRequest", None, Unset] = UNSET
    new_password: Union["NewPasswordRequest", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_password_login import EmailPasswordLogin
        from ..models.reset_pin_request import ResetPINRequest
        from ..models.reset_request import ResetRequest
        from ..models.validation_request import ValidationRequest
        from ..models.new_password_request import NewPasswordRequest

        basic_auth: Union[Dict[str, Any], None, Unset]
        if isinstance(self.basic_auth, Unset):
            basic_auth = UNSET

        elif isinstance(self.basic_auth, EmailPasswordLogin):
            basic_auth = UNSET
            if not isinstance(self.basic_auth, Unset):
                basic_auth = self.basic_auth.to_dict()

        else:
            basic_auth = self.basic_auth

        email_valid: Union[Dict[str, Any], None, Unset]
        if isinstance(self.email_valid, Unset):
            email_valid = UNSET

        elif isinstance(self.email_valid, ValidationRequest):
            email_valid = UNSET
            if not isinstance(self.email_valid, Unset):
                email_valid = self.email_valid.to_dict()

        else:
            email_valid = self.email_valid

        reset_request: Union[Dict[str, Any], None, Unset]
        if isinstance(self.reset_request, Unset):
            reset_request = UNSET

        elif isinstance(self.reset_request, ResetRequest):
            reset_request = UNSET
            if not isinstance(self.reset_request, Unset):
                reset_request = self.reset_request.to_dict()

        else:
            reset_request = self.reset_request

        reset_pin_request: Union[Dict[str, Any], None, Unset]
        if isinstance(self.reset_pin_request, Unset):
            reset_pin_request = UNSET

        elif isinstance(self.reset_pin_request, ResetPINRequest):
            reset_pin_request = UNSET
            if not isinstance(self.reset_pin_request, Unset):
                reset_pin_request = self.reset_pin_request.to_dict()

        else:
            reset_pin_request = self.reset_pin_request

        new_password: Union[Dict[str, Any], None, Unset]
        if isinstance(self.new_password, Unset):
            new_password = UNSET

        elif isinstance(self.new_password, NewPasswordRequest):
            new_password = UNSET
            if not isinstance(self.new_password, Unset):
                new_password = self.new_password.to_dict()

        else:
            new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if basic_auth is not UNSET:
            field_dict["basic_auth"] = basic_auth
        if email_valid is not UNSET:
            field_dict["email_valid"] = email_valid
        if reset_request is not UNSET:
            field_dict["reset_request"] = reset_request
        if reset_pin_request is not UNSET:
            field_dict["reset_pin_request"] = reset_pin_request
        if new_password is not UNSET:
            field_dict["new_password"] = new_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_password_login import EmailPasswordLogin
        from ..models.reset_pin_request import ResetPINRequest
        from ..models.reset_request import ResetRequest
        from ..models.validation_request import ValidationRequest
        from ..models.new_password_request import NewPasswordRequest

        d = src_dict.copy()

        def _parse_basic_auth(data: object) -> Union["EmailPasswordLogin", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _basic_auth_type_0 = data
                basic_auth_type_0: Union[Unset, EmailPasswordLogin]
                if isinstance(_basic_auth_type_0, Unset):
                    basic_auth_type_0 = UNSET
                else:
                    basic_auth_type_0 = EmailPasswordLogin.from_dict(_basic_auth_type_0)

                return basic_auth_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EmailPasswordLogin", None, Unset], data)

        basic_auth = _parse_basic_auth(d.pop("basic_auth", UNSET))

        def _parse_email_valid(data: object) -> Union["ValidationRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _email_valid_type_0 = data
                email_valid_type_0: Union[Unset, ValidationRequest]
                if isinstance(_email_valid_type_0, Unset):
                    email_valid_type_0 = UNSET
                else:
                    email_valid_type_0 = ValidationRequest.from_dict(
                        _email_valid_type_0
                    )

                return email_valid_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ValidationRequest", None, Unset], data)

        email_valid = _parse_email_valid(d.pop("email_valid", UNSET))

        def _parse_reset_request(data: object) -> Union["ResetRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _reset_request_type_0 = data
                reset_request_type_0: Union[Unset, ResetRequest]
                if isinstance(_reset_request_type_0, Unset):
                    reset_request_type_0 = UNSET
                else:
                    reset_request_type_0 = ResetRequest.from_dict(_reset_request_type_0)

                return reset_request_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResetRequest", None, Unset], data)

        reset_request = _parse_reset_request(d.pop("reset_request", UNSET))

        def _parse_reset_pin_request(
            data: object,
        ) -> Union["ResetPINRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _reset_pin_request_type_0 = data
                reset_pin_request_type_0: Union[Unset, ResetPINRequest]
                if isinstance(_reset_pin_request_type_0, Unset):
                    reset_pin_request_type_0 = UNSET
                else:
                    reset_pin_request_type_0 = ResetPINRequest.from_dict(
                        _reset_pin_request_type_0
                    )

                return reset_pin_request_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResetPINRequest", None, Unset], data)

        reset_pin_request = _parse_reset_pin_request(d.pop("reset_pin_request", UNSET))

        def _parse_new_password(
            data: object,
        ) -> Union["NewPasswordRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _new_password_type_0 = data
                new_password_type_0: Union[Unset, NewPasswordRequest]
                if isinstance(_new_password_type_0, Unset):
                    new_password_type_0 = UNSET
                else:
                    new_password_type_0 = NewPasswordRequest.from_dict(
                        _new_password_type_0
                    )

                return new_password_type_0
            except:  # noqa: E722
                pass
            return cast(Union["NewPasswordRequest", None, Unset], data)

        new_password = _parse_new_password(d.pop("new_password", UNSET))

        login_request = cls(
            basic_auth=basic_auth,
            email_valid=email_valid,
            reset_request=reset_request,
            reset_pin_request=reset_pin_request,
            new_password=new_password,
        )

        login_request.additional_properties = d
        return login_request

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
