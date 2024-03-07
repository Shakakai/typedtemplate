# TypedTemplate

A simple template engine wrapper for Python that uses Pydantic models to validate and type hint the input data.

## Installation

Basic installation w/o any extras, you need to include a supported template engine in your project dependencies:
```bash
pip install typed-template
```

Installation with Jinja2 support, will install Jinja2 as a dependency:
```bash
pip install typed-template[jinja2]
```


## Usage

### Hello World Example:

```python
from pydantic import Field
from typedtemplate import TypedTemplate, JinjaTemplateEngine

# Basic engine configuration
# This only supports string templates (no files)
# See examples below for more advanced engine configuration
engine = JinjaTemplateEngine()
    
class HelloWorldTemplate(TypedTemplate):
    # Tells the template what engine to use
    template_engine = engine
    # The template to render
    template_string = "Hello, {{ name }}!"
    # The typed input data for this template
    name: str = Field(description="The name to say hello to")

# If you don't provide `name` at creation, it will raise a ValidationError
template = HelloWorldTemplate(name="World")
# Model validation is also run when `render` is called
print(template.render()) # "Hello, World!"
```

### Jinja2 File Template Example:

```python
import os
from pydantic import Field
from typedtemplate import TypedTemplate, JinjaTemplateEngine

# Create a list of directories to look for templates in
current_directory = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_directory, "test_data")
dirs = [test_data_dir]
# Configuring Jinja2 to look for templates in a specific directory, "test_data" in this case
engine = JinjaTemplateEngine(dirs=dirs, debug=True)


class HelloWorldFileTemplate(TypedTemplate):
    # Tells the template what engine to use
    template_engine = engine
    # This will look for a file called "hello_world.jinja2" in the "test_data" directory
    # Assume the template is the same as the Hello World example above
    template_file = "hello_world.jinja2"
    # The typed input data for this template
    name: str = Field(description="The name to say hello to")

# If you don't provide `name` at creation, it will raise a ValidationError
template = HelloWorldFileTemplate(name="World")
# Model validation is also run when `render` is called
print(template.render()) # "Hello, World!"
```

### Django File Template Example:

```python
import os
from pydantic import Field
from typedtemplate import TypedTemplate, DjangoTemplateEngine

# Create a list of directories to look for templates in
current_directory = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_directory, "test_data")
dirs = [test_data_dir]
# Configuring Django to look for templates in a specific directory, "test_data" in this case
# Generally, you shouldn't use the Django templating engine without using the Django framework
# If Django templates are already configured in your django settings, you can drop the `dirs` parameter and set `skip_django_configure` to `True`
engine = DjangoTemplateEngine(dirs=dirs, debug=True, skip_django_configure=False)


class HelloWorldFileTemplate(TypedTemplate):
    # Tells the template what engine to use
    template_engine = engine
    # This will look for a file called "hello_world.txt" in the "test_data" directory
    # Assume the template is the same as the Hello World example above
    template_file = "hello_world.txt"
    # The typed input data for this template
    name: str = Field(description="The name to say hello to")

# If you don't provide `name` at creation, it will raise a ValidationError
template = HelloWorldFileTemplate(name="World")
# Model validation is also run when `render` is called
print(template.render()) # "Hello, World!"
```

### Advanced Pydantic Model Usage:

```python
from typing import Optional
from pydantic import BaseModel, Field
from typedtemplate import TypedTemplate, JinjaTemplateEngine

# Pydantic Object Model
class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    occupation: Optional[str] = None

# Basic engine configuration
engine = JinjaTemplateEngine()

template_str = """
<h1>Users</h1>
<ol>
{% for user in users %}
    <li>{{ user.first_name }} {{ user.last_name }} ({{ user.age }} years old){% if user.occupation %}: {{ user.occupation }}{% endif %}</li>
{% endfor %}
</ol>
<p>Total Users: {{ users|length }}</p>
"""
    
class UserListTemplate(TypedTemplate):
    # Tells the template what engine to use
    template_engine = engine
    # The template to render
    template_string = template_str
    # The typed input data for this template
    users: list[User] = Field(description="A list of users")

users = [
    User(first_name="John", last_name="Doe", age=30, occupation="Software Engineer"),
    User(first_name="Jane", last_name="Doe", age=28, occupation="Doctor"),
    User(first_name="Alice", last_name="Smith", age=25),
]
# If you don't provide `name` at creation, it will raise a ValidationError
template = UserListTemplate(users=users)
# Model validation is also run when `render` is called
print(template.render())
```

# Contributing

We're open to contributions! If you have any ideas, feel free to open an issue or a pull request.

# License

This repository is licensed under the MIT license. See [LICENSE](LICENSE) for details.
