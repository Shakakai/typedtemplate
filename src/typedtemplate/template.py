from typing import ClassVar, Optional
from pydantic import BaseModel
from pydantic.fields import PrivateAttr
import logging

from .engine import BaseTemplateEngine, TemplateFunc

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class TypedTemplate(BaseModel):
    template_engine: ClassVar[BaseTemplateEngine]
    template_file: ClassVar[Optional[str]] = None
    template_string: ClassVar[Optional[str]] = None
    _template: TemplateFunc = PrivateAttr(default=None)

    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)

        self._template = self.template_engine.get_template_func(
            template_str=self.template_string,
            template_file=self.template_file
        )

    def validate_context(self, context: dict) -> dict:
        ctx = {**self.model_dump(), **context}
        self.model_validate(ctx)
        return ctx

    def render(self, context: dict = None) -> str:
        context = context if context is not None else {}
        ctx = self.validate_context(context)
        result = self._template(ctx)
        return result
