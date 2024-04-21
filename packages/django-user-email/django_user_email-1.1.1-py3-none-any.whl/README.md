<h1 align="center">
  django-user-email
</h1>

<p align="center">
  <a href="https://github.com/khasbilegt/django-user-email/">
    <img src="https://img.shields.io/github/actions/workflow/status/khasbilegt/django-user-email/ci.yml?label=CI&logo=github&style=for-the-badge" alt="ci status">
  </a>
  <a href="https://pypi.org/project/django-user-email/">
    <img src="https://img.shields.io/pypi/v/django-user-email?style=for-the-badge" alt="pypi link">
  </a>
  <a href="https://codecov.io/github/khasbilegt/django-user-email">
    <img src="https://img.shields.io/codecov/c/github/khasbilegt/django-user-email?logo=codecov&style=for-the-badge" alt="codecov">
  </a>
  <br>
  <a>
    <img src="https://img.shields.io/pypi/pyversions/django-user-email?logo=python&style=for-the-badge" alt="supported python versions">
  </a>
  <a>
    <img src="https://img.shields.io/pypi/djversions/django-user-email?logo=django&style=for-the-badge" alt="supported django versions">
  </a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<p align="center">Custom, simple Django User model with email as username</p>

## Installation

1. Use your preferred package manager ([pip](https://pip.pypa.io/en/stable/), [poetry](https://pypi.org/project/poetry/), [pipenv](https://pypi.org/project/pipenv/)) to install the package. For example:

```bash
$ poetry add django-user-email
```

2. Then register 'user_email', in the 'INSTALLED_APPS' section of your project's settings.

```python
# settings.py
...

INSTALLED_APPS = (
    ...
    'user_email',
)

...
```

3. Set AUTH_USER_MODEL - Since it's a custom User model Django needs to know the path of the model

```bash
# settings.py
...

AUTH_USER_MODEL = 'user_email.User'

...
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
