import os
from typing import ClassVar, Type

import pytest
from typedtemplate import TypedTemplate, DjangoTemplateEngine, JinjaTemplateEngine
from pydantic import Field


def pytest_sessionstart(session):
    """
    Initialize the Django settings for testing.
    :param session:
    :return:
    """
    from django.conf import settings
    settings.configure(
        DEBUG=True,
    )


def get_dirs():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(current_directory, "test_data")
    dirs = [test_data_dir]
    return dirs


@pytest.fixture(name="django_engine")
def get_django_engine():
    dirs = get_dirs()
    return DjangoTemplateEngine(dirs=dirs, debug=True, skip_django_configure=True)


@pytest.fixture(name="jinja_engine")
def get_jinja_engine():
    dirs = get_dirs()
    return JinjaTemplateEngine(dirs=dirs, debug=True)


@pytest.fixture(name="string_template")
def get_string_template(django_engine: DjangoTemplateEngine) -> Type[TypedTemplate]:
    class StringTemplate(TypedTemplate):
        template_engine = django_engine
        template_string: ClassVar[str] = "Hello, {{ name }}!"
        name: str = Field(description="Person's name.")

    return StringTemplate


@pytest.fixture(name="file_template")
def get_file_template(django_engine: DjangoTemplateEngine) -> Type[TypedTemplate]:
    class FileTemplate(TypedTemplate):
        template_engine = django_engine
        template_file: ClassVar[str] = "test_template.txt"
        name: str = Field(description="Person's name.")

    return FileTemplate
