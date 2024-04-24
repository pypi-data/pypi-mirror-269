# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_tabbed_structblock', 'wagtail_tabbed_structblock.migrations']

package_data = \
{'': ['*'],
 'wagtail_tabbed_structblock': ['static/tabbed_structblock/css/*',
                                'static/tabbed_structblock/js/*',
                                'templates/tabbed_structblock/*']}

setup_kwargs = {
    'name': 'wagtail-tabbed-structblock',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Eric Kersten',
    'author_email': 'eric.kersten@egodesign.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
