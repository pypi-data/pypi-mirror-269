# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocflib',
 'ocflib.account',
 'ocflib.infra',
 'ocflib.lab',
 'ocflib.misc',
 'ocflib.org',
 'ocflib.printing',
 'ocflib.ucb',
 'ocflib.vhost']

package_data = \
{'': ['*'], 'ocflib.account': ['mail_templates/*']}

install_requires = \
['attrs>=22.2.0',
 'cached-property>=1.5.2,<2.0.0',
 'cracklib>=2.9.6,<3.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'jinja2>=3.0.3,<4.0.0',
 'ldap3>=2.9.1,<3.0.0',
 'pexpect>=4.9.0,<5.0.0',
 'pycryptodome>=3.19.0,<4.0.0',
 'pygithub>=1.56',
 'pymysql>=1.0.2,<2.0.0',
 'pysnmp>=4.4.12,<5.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'redis>=4.3.6',
 'requests>=2.26.1,<3.0.0',
 'sqlalchemy>=1.4.52,<2.0.0']

setup_kwargs = {
    'name': 'ocflib',
    'version': '2024.3.14',
    'description': 'libraries for account and server management',
    'long_description': "# ocflib\n\n[![Build Status](https://jenkins.ocf.berkeley.edu/buildStatus/icon?job=ocf/ocflib/master)](https://jenkins.ocf.berkeley.edu/job/ocf/job/ocflib/job/master)\n[![Coverage Status](https://coveralls.io/repos/github/ocf/ocflib/badge.svg?branch=master)](https://coveralls.io/github/ocf/ocflib?branch=master)\n[![PyPI version](https://badge.fury.io/py/ocflib.svg)](https://pypi.org/project/ocflib/)\n\nocflib is a Python library for working with [Open Computing Facility][ocf]\nservices (in particular, accounts and server management).\n\nThe library targets Python 3.5.3 and 3.7 (the versions available in Debian\nstretch and buster).\n\nThe goal of the library is to make it easier to re-use OCF python code. In the\npast, code was split between approve, atool, create, chpass, sorry, signat,\netc., which made it difficult to do things like share common password\nrequirements.\n\n## What belongs here\n\nIn general, code which can be re-used should be here, but standalone\napplications or binaries shouldn't. For example, [ocfweb][ocfweb] uses ocflib\ncode to change passwords and create accounts, but the Django web app doesn't\nbelong here.\n\n## Using on OCF\n\nocflib is installed by [Puppet][puppet] on the OCF, so you can simply do things\nlike `import ocflib.lab.stats` from the system python3 installation. We _don't_\ninstall it to python2 site-packages.\n\nWe build [a Debian package][debian-pkg] which is installed by Puppet. We also\npublish new versions to [PyPI][pypi], which is useful because it allows easy\ninstallation into virtualenvs.\n\n## Note about lockfiles\n\nThis repository includes a `poetry.lock` file. Lockfiles are usually used to\nensure that the exact same versions of dependencies are installed across\ndifferent machines. However, as this is a library, we don't want to force\ndownstream users to use the exact same versions of dependencies as us, and\nindeed, the lockfile is ignored when distributing. We still include it in the\nrepository to make it easier to develop, test, and debug ocflib.\n\n## Installing locally\n\n### For Testing Changes\n\nDevelopment of ocflib uses [Poetry](https://python-poetry.org/). The easiest way\nto test changes to ocflib is to let Poetry manage the virtual environment for\nyou:\n\n    poetry install\n    poetry shell\n\nNow, if you import something from ocflib, you'll be using the version from your\nworking copy.\n\n### Testing and linting\n\nWe use pytest to test our code, and pre-commit to lint it. You should run\n`make test` before pushing to run both.\n\nThe `tests` directory contains automated tests which you're encouraged to add to\n(and not break). The `tests-manual` directory contains scripts intended for\ntesting.\n\n#### Using pre-commit\n\nWe use [pre-commit][pre-commit] to lint our code before commiting. While some of\nthe rules might seem a little arbitrary, it helps keep the style consistent, and\nensure annoying things like trailing whitespace don't creep in.\n\nYou can simply run `make install-hooks` to install the necessary git hooks; once\ninstalled, pre-commit will run every time you commit.\n\nAlternatively, if you'd rather not install any hooks, you can simply use\n`make test` as usual, which will also run the hooks.\n\n### Troubleshooting: Cracklib Error\n\nIf you're trying to run make install-hooks on ocfweb (or related repos) and get\nthis error:\n\n```\n./_cracklib.c:40:10: fatal error: 'crack.h' file not found\n  #include <crack.h>\n           ^~~~~~~~~\n  1 error generated.\n```\n\nThe issue relates to the cracklib package not finding the necessary header files\nto install. Make sure cracklib is installed on your machine\n(https://github.com/cracklib/cracklib, if you're on Mac,\n`brew install cracklib`).\n\n## Deploying changes\n\nDeploying changes involves:\n\n- Running tests and linters\n- Pushing a new version to [PyPI][pypi]\n- Building a Debian package\n- Pushing the Debian package to our internal [apt][apt]\n\n[Jenkins][jenkins] will automatically perform all of these steps for you on\nevery push, including automatically generating a new version number. As long as\n`make test` passes, your code will be automatically deployed. You can monitor\nthe progress of your deploy [here][jenkins].\n\n[ocf]: https://www.ocf.berkeley.edu/\n[ocfweb]: https://github.com/ocf/ocfweb/\n[puppet]: https://github.com/ocf/puppet/\n[pypi]: https://pypi.python.org/pypi/ocflib\n[apt]: http://apt.ocf.berkeley.edu/\n[jenkins]: https://jenkins.ocf.berkeley.edu/view/ocflib-deploy/\n[debian-pkg]: http://apt.ocf.berkeley.edu/pool/main/p/python-ocflib/\n[pre-commit]: http://pre-commit.com/\n",
    'author': 'Open Computing Facility',
    'author_email': 'help@ocf.berkeley.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
