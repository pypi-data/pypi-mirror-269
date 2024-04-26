from typing import Any, Dict, List

from .constants import SCHEMA_NAME


def _clean(raw: str) -> str:
    return raw.strip('"')


def _field_description(field: Dict[str, Any]) -> str:
    context: Dict[str, str] = {}

    field_definition: Dict[str, str] = field.get("FieldDefinition") or {}
    if description := field_definition.get("Description"):
        context["Description"] = _clean(description)
    if help_text := field.get("InlineHelpText"):
        context["Help Text"] = _clean(help_text)
    if compliance_group := field_definition.get("ComplianceGroup"):
        context["Compliance Categorization"] = _clean(compliance_group)
    if security_level := field_definition.get("SecurityClassification"):
        context["Data Sensitivity Level"] = _clean(security_level)

    return "\n".join([f"- {k}: {v}" for k, v in context.items()])


def _to_column_payload(field: dict, position: int, table_name: str) -> dict:
    field_name = field["QualifiedApiName"]
    return {
        "id": f"{table_name}.{field_name}",
        "table_id": table_name,
        "column_name": field_name,
        "description": _field_description(field),
        "data_type": field.get("DataType"),
        "ordinal_position": position,
    }


def _to_table_payload(table: dict) -> dict:
    return {
        "id": table["QualifiedApiName"],
        "schema_id": SCHEMA_NAME,
        "table_name": table["QualifiedApiName"],
        "description": "",
        "tags": [],
        "type": "TABLE",
    }


class SalesforceFormatter:
    """
    Helper functions that format the response in the format to be exported as
    csv.
    """

    @staticmethod
    def tables(sobjects: List[dict]) -> List[dict]:
        """formats the raw list of sobjects to tables"""
        return [_to_table_payload(s) for s in sobjects]

    @staticmethod
    def columns(sobject_fields: Dict[str, List[dict]]) -> List[dict]:
        """formats the raw list of sobject fields to columns"""
        return [
            _to_column_payload(field, idx, table_name)
            for table_name, fields in sobject_fields.items()
            for idx, field in enumerate(fields)
        ]
