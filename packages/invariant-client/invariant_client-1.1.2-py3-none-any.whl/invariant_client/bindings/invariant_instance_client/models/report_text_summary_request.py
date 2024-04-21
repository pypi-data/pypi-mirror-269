from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union


T = TypeVar("T", bound="ReportTextSummaryRequest")


@_attrs_define
class ReportTextSummaryRequest:
    """
    Attributes:
        mode (Union[Unset, str]):  Default: 'text'.
        traces (Union[Unset, bool]):
    """

    mode: Union[Unset, str] = "text"
    traces: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mode = self.mode
        traces = self.traces

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if traces is not UNSET:
            field_dict["traces"] = traces

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mode = d.pop("mode", UNSET)

        traces = d.pop("traces", UNSET)

        report_text_summary_request = cls(
            mode=mode,
            traces=traces,
        )

        report_text_summary_request.additional_properties = d
        return report_text_summary_request

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
