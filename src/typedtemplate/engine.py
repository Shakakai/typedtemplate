from typing import List, Callable, Union
from pydantic import BaseModel

TemplateFunc = Callable[[Union[dict, BaseModel]], str]


class BaseTemplateEngine:
    """
    This is the base class for Template Engines.
    Subclasses should configure their template engine in the __init__ method, passing in any required configuration.
    render should be implemented to take a template and context and return the rendered template.
    """

    def get_template_func(self, template_str: str = None, template_file: str = None) -> TemplateFunc:
        raise NotImplementedError("Subclasses must implement this method.")

    def get_template_string(self, template_file: str = None) -> str:
        raise NotImplementedError("Subclasses must implement this method.")


class DjangoTemplateEngine(BaseTemplateEngine):
    """
    This is a Django Template Engine.
    """

    def __init__(self, dirs: List[str] = None, debug: bool = False, skip_django_configure: bool = False):
        try:
            from django.template import Engine
            from django.conf import settings
        except ImportError:
            raise ImportError("Django is not installed. Please install Django to use this template engine.")

        if not skip_django_configure:
            settings.configure(
                DEBUG=debug,
            )

        self.engine = Engine(
            dirs=dirs,
            app_dirs=False,
            context_processors=None,
            debug=debug,
            loaders=None,
            string_if_invalid="",
            file_charset="utf-8",
            libraries=None,
            builtins=Engine.default_builtins,
            autoescape=False,
        )

    def get_template_func(self, template_str: str = None, template_file: str = None) -> TemplateFunc:
        template = None
        if template_str:
            template = self.engine.from_string(template_str)
        elif template_file:
            template = self.engine.get_template(template_file)
        else:
            raise Exception("Either template_str or template_file must be defined.")

        def template_func(model: Union[BaseModel, dict]) -> str:
            try:
                from django.template import Context
            except ImportError:
                raise ImportError("Django is not installed. Please install Django to use this template engine.")
            if not isinstance(model, dict):
                model = model.model_dump()
            context = Context(model)
            return template.render(context)

        return template_func


class JinjaTemplateEngine(BaseTemplateEngine):
    """
    This is a Jinja Template Engine.
    """

    def __init__(self, dirs: List[str] = None, debug: bool = False):
        try:
            from jinja2 import Environment, FileSystemLoader
        except ImportError:
            raise ImportError("Jinja2 is not installed. Please install Jinja2 to use this template engine.")

        if dirs is None:
            dirs = []

        self.env = Environment(loader=FileSystemLoader(dirs), autoescape=False)

    def get_template_func(self, template_str: str = None, template_file: str = None) -> TemplateFunc:
        template = None
        if template_str:
            template = self.env.from_string(template_str)
        elif template_file:
            template = self.env.get_template(template_file)
        else:
            raise Exception("Either template_str or template_file must be defined.")

        def template_func(model: Union[BaseModel, dict]) -> str:
            return template.render(model)

        return template_func
