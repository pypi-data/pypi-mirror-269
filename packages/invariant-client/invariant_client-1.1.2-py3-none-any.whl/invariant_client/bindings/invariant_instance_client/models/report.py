from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
from typing import Union
from typing import Dict
import datetime

if TYPE_CHECKING:
    from ..models.poc_report_data import POCReportData
    from ..models.snapshot_report_data import SnapshotReportData


T = TypeVar("T", bound="Report")


@_attrs_define
class Report:
    """
    Attributes:
        uuid (str):
        organization_uuid (str):
        reports (Union['POCReportData', 'SnapshotReportData']):
        created_at (datetime.datetime):
    """

    uuid: str
    organization_uuid: str
    reports: Union["POCReportData", "SnapshotReportData"]
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.snapshot_report_data import SnapshotReportData

        uuid = self.uuid
        organization_uuid = self.organization_uuid
        reports: Dict[str, Any]

        if isinstance(self.reports, SnapshotReportData):
            reports = self.reports.to_dict()

        else:
            reports = self.reports.to_dict()

        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "organization_uuid": organization_uuid,
                "reports": reports,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.poc_report_data import POCReportData
        from ..models.snapshot_report_data import SnapshotReportData

        d = src_dict.copy()
        uuid = d.pop("uuid")

        organization_uuid = d.pop("organization_uuid")

        def _parse_reports(
            data: object,
        ) -> Union["POCReportData", "SnapshotReportData"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reports_type_0 = SnapshotReportData.from_dict(data)

                return reports_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            reports_type_1 = POCReportData.from_dict(data)

            return reports_type_1

        reports = _parse_reports(d.pop("reports"))

        created_at = isoparse(d.pop("created_at"))

        report = cls(
            uuid=uuid,
            organization_uuid=organization_uuid,
            reports=reports,
            created_at=created_at,
        )

        report.additional_properties = d
        return report

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
