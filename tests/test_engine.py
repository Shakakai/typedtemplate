
from typedtemplate import DjangoTemplateEngine, JinjaTemplateEngine


def test_django_engine(django_engine: DjangoTemplateEngine):
    template_func = django_engine.get_template_func(template_str="Hello, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"


def test_multi_usage_django(django_engine: DjangoTemplateEngine):
    template_func = django_engine.get_template_func(template_str="Hello, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"
    template_func = django_engine.get_template_func(template_str="Hi, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hi, Todd!"


def test_django_template_func(django_engine: DjangoTemplateEngine):
    template_func = django_engine.get_template_func(template_str="Hello, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"
    result = template_func({"name": "Bob"})
    assert result == "Hello, Bob!"


def test_django_file_template(django_engine: DjangoTemplateEngine):
    template_func = django_engine.get_template_func(template_file="test_template.txt")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"


def test_jinja_engine(jinja_engine: JinjaTemplateEngine):
    template_func = jinja_engine.get_template_func(template_str="Hello, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"


def test_multi_usage_jinja(jinja_engine: JinjaTemplateEngine):
    template_func = jinja_engine.get_template_func(template_str="Hello, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"
    template_func = jinja_engine.get_template_func(template_str="Hi, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hi, Todd!"


def test_jinja_template_func(jinja_engine: JinjaTemplateEngine):
    template_func = jinja_engine.get_template_func(template_str="Hello, {{ name }}!")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"
    result = template_func({"name": "Bob"})
    assert result == "Hello, Bob!"


def test_jinja_file_template(jinja_engine: JinjaTemplateEngine):
    template_func = jinja_engine.get_template_func(template_file="test_template.txt")
    assert template_func
    result = template_func({"name": "Todd"})
    assert result == "Hello, Todd!"
