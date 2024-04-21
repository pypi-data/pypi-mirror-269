from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from typing import cast
from typing import Dict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.comparison_reportdata_files import ComparisonReportdataFiles


T = TypeVar("T", bound="ComparisonReportdata")


@_attrs_define
class ComparisonReportdata:
    """
    Attributes:
        files (ComparisonReportdataFiles):
        solutions (Union[None, Unset, str]):
    """

    files: "ComparisonReportdataFiles"
    solutions: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        files = self.files.to_dict()

        solutions: Union[None, Unset, str]
        if isinstance(self.solutions, Unset):
            solutions = UNSET

        else:
            solutions = self.solutions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
            }
        )
        if solutions is not UNSET:
            field_dict["solutions"] = solutions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.comparison_reportdata_files import ComparisonReportdataFiles

        d = src_dict.copy()
        files = ComparisonReportdataFiles.from_dict(d.pop("files"))

        def _parse_solutions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        solutions = _parse_solutions(d.pop("solutions", UNSET))

        comparison_reportdata = cls(
            files=files,
            solutions=solutions,
        )

        comparison_reportdata.additional_properties = d
        return comparison_reportdata

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
