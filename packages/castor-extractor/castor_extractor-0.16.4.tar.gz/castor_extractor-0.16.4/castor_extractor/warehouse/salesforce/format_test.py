from .format import _field_description


def test__field_description():

    field = {}
    assert _field_description(field) == ""

    definition = {}
    field = {"FieldDefinition": definition}
    assert _field_description(field) == ""

    definition.update({"Description": "foo"})
    assert "foo" in _field_description(field)

    field.update({"InlineHelpText": "bar"})
    assert "bar" in _field_description(field)

    definition.update({"ComplianceGroup": "bim"})
    assert "bim" in _field_description(field)

    definition.update({"SecurityClassification": "bam"})
    description = _field_description(field)

    assert "bam" in description
    expected = (
        "- Description: foo\n"
        "- Help Text: bar\n"
        "- Compliance Categorization: bim\n"
        "- Data Sensitivity Level: bam"
    )
    assert description == expected
