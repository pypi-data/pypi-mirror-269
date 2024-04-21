from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="UploadSnapshotStatusResponse")


@_attrs_define
class UploadSnapshotStatusResponse:
    """
    Attributes:
        is_running (bool):
        terminated (bool):
    """

    is_running: bool
    terminated: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_running = self.is_running
        terminated = self.terminated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_running": is_running,
                "terminated": terminated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_running = d.pop("is_running")

        terminated = d.pop("terminated")

        upload_snapshot_status_response = cls(
            is_running=is_running,
            terminated=terminated,
        )

        upload_snapshot_status_response.additional_properties = d
        return upload_snapshot_status_response

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
