# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dspy_dummy']

package_data = \
{'': ['*']}

install_requires = \
['dspy-ai==2.4.5']

setup_kwargs = {
    'name': 'dspy',
    'version': '0.1.5',
    'description': 'Placeholder package for DSPy',
    'long_description': '',
    'author': 'Tom Dörr',
    'author_email': 'tomdoerr96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
