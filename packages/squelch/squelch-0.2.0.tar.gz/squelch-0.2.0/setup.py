# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squelch']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=2.0.29,<3.0.0', 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['squelch = squelch.__main__:main']}

setup_kwargs = {
    'name': 'squelch',
    'version': '0.2.0',
    'description': 'Simple SQL REPL Command Handler',
    'long_description': '# squelch\n\nSquelch is a package providing a Simple SQL REPL Command Handler.  Squelch uses SQLAlchemy for database access and so can support any database engine that SQLAlchemy supports, thereby providing a common database client experience for any of those database engines.  Squelch is modelled on a simplified `psql`, the PostgreSQL command line client.  The Squelch CLI supports readline history and basic SQL statement tab completions.\n\n## Install\n\nThe package can be installed from PyPI:\n\n```bash\n$ pip install squelch\n```\n\n## From the command line\n\nThe package comes with a functional CLI called `squelch`, which just calls the package *main*, hence the following two invocations are equivalent:\n\n```bash\n$ python3 -m squelch\n```\n\n```bash\n$ squelch\n```\n\nThe only required argument is a database connection URL.  This can either be passed on the command line, via the `--url` option, or specified in a JSON configuration file given by the `--conf-file` option.  The form of the JSON configuration file is as follows:\n\n```json\n{\n  "url": "<URL>"\n}\n```\n\nwhere the `<URL>` follows the [SQLAlchemy database connection URL syntax](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).  An advantage of using a configuration file is that it avoids providing database login credentials in plain text on the command line.\n\n### Command line usage\n\n```\nusage: squelch [-h] [-c CONF_FILE] [-u URL] [-v] [-V]\n\nSquelch is a Simple SQL REPL Command Handler.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONF_FILE, --conf-file CONF_FILE\n                        The full path to a JSON configuration file. It\n                        defaults to ./squelch.json.\n  -u URL, --url URL     The database connection URL, as required by\n                        sqlalchemy.create_engine().\n  -v, --verbose         Turn verbose messaging on. The effects of this option\n                        are incremental.\n  -V, --version         show program\'s version number and exit\n\nDatabase Connection URL\n\nThe database connection URL can either be passed on the command line, via the --url option, or specified in a JSON configuration file given by the --conf-file option.  The form of the JSON configuration file is as follows:\n\n{\n  "url": "<URL>"\n}\n\nFrom the SQLAlchemy documentation:\n\n"The string form of the URL is dialect[+driver]://user:password@host/dbname[?key=value..], where dialect is a database name such as mysql, oracle, postgresql, etc., and driver the name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc. Alternatively, the URL can be an instance of URL."\n```\n\n',
    'author': 'Paul Breen',
    'author_email': 'pbree@bas.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/paul-breen/squelch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
