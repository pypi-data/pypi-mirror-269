# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol',
 'exasol.saas.client',
 'exasol.saas.client.openapi',
 'exasol.saas.client.openapi.api',
 'exasol.saas.client.openapi.api.clusters',
 'exasol.saas.client.openapi.api.databases',
 'exasol.saas.client.openapi.api.files',
 'exasol.saas.client.openapi.api.platform',
 'exasol.saas.client.openapi.api.profile',
 'exasol.saas.client.openapi.api.security',
 'exasol.saas.client.openapi.api.usage',
 'exasol.saas.client.openapi.api.users',
 'exasol.saas.client.openapi.models']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.2.0,<0.3.0',
 'requests>=2.31.0,<3.0.0',
 'types-requests>=2.31.0.6,<3.0.0.0']

entry_points = \
{'console_scripts': ['tbx = exasol.toolbox.tools.tbx:CLI']}

setup_kwargs = {
    'name': 'saas-api',
    'version': '0.1.0',
    'description': 'API enabling Python applications connecting to Exasol database SaaS instances and using their SaaS services',
    'long_description': '# SaaS API for Python\n\nAPI enabling Python applications connecting to Exasol database SaaS instances and using their SaaS services.\n\nThe model layer of this API is generated from the OpenAPI specification in JSON format of the SaaS API https://cloud.exasol.com/openapi.json using [openapi-python-client](https://github.com/openapi-generators/openapi-python-client).\n\nA GitHub action will check each morning if the generated model layer is outdated.\n\nSee\n* [User Guide](doc/user_guide/user-guide.md)\n* [Developer Guide](doc/developer_guide/developer_guide.md)\n',
    'author': 'Christoph Kuhnke',
    'author_email': 'christoph.kuhnke@exasol.com',
    'maintainer': 'Christoph Kuhnke',
    'maintainer_email': 'christoph.kuhnke@exasol.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
