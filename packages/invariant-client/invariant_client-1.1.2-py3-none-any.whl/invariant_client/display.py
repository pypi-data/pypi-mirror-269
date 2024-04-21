import enum
import json
from attr import asdict
import pandas
from tabulate import tabulate
from invariant_client.bindings.invariant_instance_client.models.get_report_summary_response import GetReportSummaryResponse


class OutputFormat(enum.Enum):
    TABULATE = enum.auto()
    JSON = enum.auto()
    TSV = enum.auto()
    # etc


def snapshot_status(response: GetReportSummaryResponse):
    """Display a message indicating the overall status of the analysis user task."""
    status = response.status.to_dict()
    status = status.get('state')
    if status == 'COMPLETE':
        pass
    elif status == 'FAILED':
        print("Error: Snapshot could not be evaluated.")
    elif status == 'INCOMPLETE':
        print("Error: Snapshot evaluation did not finish.")


def snapshot_summary_table(response: GetReportSummaryResponse, format: OutputFormat):
    """Display a table containing row counts for all emitted reports."""
    if format == OutputFormat.JSON:
        pass
    else:
        print_frame(pandas.DataFrame(response.summary.to_dict().items(), columns=['File', 'RowCount']), format)


def snapshot_halted(response: GetReportSummaryResponse):
    """Describe each halted step."""
    status = response.status.to_dict()
    halted = []
    def visit_step(step: dict, prefix: list):
        prefix = prefix + [step['name']] if prefix else [step['name']]
        if step['state'] != 'COMPLETE':
            halted.append((prefix, step))
        for child_step in step['steps']:
            visit_step(child_step, prefix)
    visit_step(status, None)
    if len(halted):
        print("\nThe following steps were not completed:")
        for prefix, step in halted:
            print(f"    {' > '.join(prefix)}")
            if step['state'] != 'FAILED':
                print(f"\n        {step['state']}")


def snapshot_errors(errors: pandas.DataFrame, format: OutputFormat):
    """Describe each error."""
    # Group errors by label, then repeat the header every 10th member
    for label, error_group in errors.groupby(by=['label']):
        label = label[0]
        for i, error in enumerate(error_group.to_dict(orient='records')):
            prefix = ""
            if not i % 10:
                prefix = f"In {label}{' (continued)' if i > 0 else ''}:\n\n"
            data = json.loads(error['detail'])
            if data['type'] == 'urn:invariant:errors:child_step_failed':
                continue
            if data['type'] == 'urn:invariant:errors:internal_exception':
                print(f"\nInternal error in {label}:\n    {data['detail']}")
                continue

            print(f"\n{prefix}    {data['title']}\n    {data['detail']}")


def print_frame(data: pandas.DataFrame, format: OutputFormat):
    if format == OutputFormat.TSV:
        print(tabulate(data, headers='keys', tablefmt='tsv'))
    elif format == OutputFormat.TABULATE:
        print(tabulate(data, headers='keys', tablefmt='psql'))
    else:
        raise ValueError(f"Unacceptable format: {format}")
