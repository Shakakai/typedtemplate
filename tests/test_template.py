from typing import Type
import pytest
from typedtemplate import TypedTemplate


def test_string_template(string_template: Type[TypedTemplate]):
    template = string_template(name="Todd")
    result = template.render()
    assert result == "Hello, Todd!"


def test_file_template(file_template: Type[TypedTemplate]):
    template = file_template(name="Todd")
    result = template.render()
    assert result == "Hello, Todd!"


def test_template_failure(string_template: Type[TypedTemplate]):
    with pytest.raises(Exception):
        string_template()
        assert False, "Should throw an error due to missing name property"


def test_template_failure_property_change(string_template: Type[TypedTemplate]):
    with pytest.raises(Exception):
        template = string_template(name="Todd")
        template.name = None
        template.render()
        assert False, "Render should throw an error due to missing name property"
