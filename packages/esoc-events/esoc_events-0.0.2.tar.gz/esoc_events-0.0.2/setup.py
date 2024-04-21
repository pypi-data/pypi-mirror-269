# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['esoc_events', 'esoc_events.utils']

package_data = \
{'': ['*']}

install_requires = \
['pytest-html>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'esoc-events',
    'version': '0.0.2',
    'description': 'Querying events comming from ESOC sources',
    'long_description': "# esoc_events\n\n[![PyPI](https://img.shields.io/pypi/v/esoc_events?style=flat-square)](https://pypi.python.org/pypi/esoc_events/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/esoc_events?style=flat-square)](https://pypi.python.org/pypi/esoc_events/)\n[![PyPI - License](https://img.shields.io/pypi/l/esoc_events?style=flat-square)](https://pypi.python.org/pypi/esoc_events/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n\n---\n\n**Documentation**: [https://r-andres.github.io/esoc_events](https://r-andres.github.io/esoc_events)\n\n**Source Code**: [https://github.com/r-andres/esoc_events](https://github.com/r-andres/esoc_events)\n\n**PyPI**: [https://pypi.org/project/esoc_events/](https://pypi.org/project/esoc_events/)\n\n---\n\nQuerying events comming from ESOC sources\n\n## Installation\n\n```sh\npip install esoc_events\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/r-andres/esoc_events/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/r-andres/esoc_events/releases) and publish it. When\n a release is published, it'll trigger [release](https://github.com/r-andres/esoc_events/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nThis project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.\n",
    'author': 'Rafael Andres',
    'author_email': 'r.andres.blasco@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://r-andres.github.io/esoc_events',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
