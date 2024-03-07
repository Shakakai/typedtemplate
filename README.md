# TypedTemplate

A simple template engine wrapper for Python that uses Pydantic models to validate and type hint the input data.

## Installation

Basic installation w/o any extras, you need to include a supported template engine in your project dependencies:
```bash
pip install typedtemplate
```

Installation with Jinja2 support, will install Jinja2 as a dependency:
```bash
pip install typedtemplate[jinja2]
```

## Support Template Engines 

We currently support the following template engines:
- [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)
- [Django](https://docs.djangoproject.com/en/3.2/topics/templates/)

If you'd like to see support for another template engine, please open an issue or a pull request.

## Usage

### Hello World Example

A basic example using a string template defined in python.

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

### Jinja2 File Template Example

This examples shows how to configure Jinja2 to look for templates in a specific directory.
Note, this example also turns debugging on, which will print warnings and errors to console.
The template is specified via the `template_file` attribute, which is the file name of the template to look for in the configured directories.

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

### Django File Template Example

This examples shows how to configure Django to look for templates in a specific directory.
In most cases, you will only use Django templates with the Django framework. 
This example assumes you ARE NOT using the Django framework and calls the `settings.configure` method to configure Django for you.
If you are using the Django framework, please look at the next example for the subtle difference.

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

### Use with the Django Web Framework
This example assume you are using the Django web framework.
You should have already configured your Django settings to look for templates in a specific directory.
See the Django documentation for more information on template directory configuration [https://docs.djangoproject.com/en/5.0/topics/templates/#configuration](https://docs.djangoproject.com/en/5.0/topics/templates/#configuration)

```python
import os
from pydantic import Field
from typedtemplate import TypedTemplate, DjangoTemplateEngine

# Tells the engine to use the already configured Django settings
engine = DjangoTemplateEngine(skip_django_configure=True)


class HelloWorldFileTemplate(TypedTemplate):
    # Tells the template what engine to use
    template_engine = engine
    # This will look for a file called "hello_world.txt" in directories configured in your Django settings
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

This repository is licensed under the MIT license. See [LICENSE](https://raw.githubusercontent.com/Shakakai/typedtemplate/main/LICENSE) for details.
