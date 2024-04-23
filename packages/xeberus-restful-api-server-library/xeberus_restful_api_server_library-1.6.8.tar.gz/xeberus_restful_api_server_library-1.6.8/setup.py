# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.xeberus',
 'majormode.xeberus.service',
 'majormode.xeberus.service.device']

package_data = \
{'': ['*'],
 'majormode.xeberus.service.device': ['db/create_device_constraint.sql',
                                      'db/create_device_constraint.sql',
                                      'db/create_device_constraint.sql',
                                      'db/create_device_index.sql',
                                      'db/create_device_index.sql',
                                      'db/create_device_index.sql',
                                      'db/create_device_table.sql',
                                      'db/create_device_table.sql',
                                      'db/create_device_table.sql',
                                      'doc/api/*',
                                      'doc/api/backup/*']}

install_requires = \
['fabric>=2.7.0,<3.0.0',
 'perseus-core-library>=1.20.3,<2.0.0',
 'perseus-restful-api-framework>=1.28.4,<2.0.0',
 'xeberus-core-library']

setup_kwargs = {
    'name': 'xeberus-restful-api-server-library',
    'version': '1.6.8',
    'description': 'Xeberus RESTful API Server Python Library',
    'long_description': '# Xeberus RESTful API Server Python Library\n\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/xeberus-restful-api-server-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
