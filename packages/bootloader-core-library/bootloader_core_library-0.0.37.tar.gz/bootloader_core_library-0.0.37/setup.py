# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootloader',
 'bootloader.scooby',
 'bootloader.scooby.constant',
 'bootloader.scooby.model']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19,<2.0']

setup_kwargs = {
    'name': 'bootloader-core-library',
    'version': '0.0.37',
    'description': 'Repository of reusable Python components to be shared by Python projects using the Bootloader services',
    'long_description': '# Bootloader Core Python Library\n\nRepository of reusable Python components to be shared by Python projects using the Bootloader services.\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel@bootloader.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bootloader-studio/bootloader-core-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
