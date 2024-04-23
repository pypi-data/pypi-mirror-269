import pytest

from yatbaf import types


@pytest.fixture
def api_types(monkeypatch, api_spec):
    types = api_spec["types"]
    monkeypatch.delitem(types, "InputFile")
    return types


def test_type_object(api_types):
    for api_type in api_types.values():
        assert hasattr(types, api_type["name"])


def test_type_fields(api_types):
    for api_type in api_types.values():
        type_obj = getattr(types, api_type["name"])
        for field in api_type.get("fields", []):
            field_name = n if (n := field["name"]) != "from" else "from_"
            assert hasattr(type_obj, field_name)
