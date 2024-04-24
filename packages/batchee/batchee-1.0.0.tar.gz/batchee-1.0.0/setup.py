# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batcher', 'batcher.harmony']

package_data = \
{'': ['*']}

install_requires = \
['harmony-service-lib>=1.0.26,<2.0.0']

entry_points = \
{'console_scripts': ['batchee = batcher.tempo_filename_parser:main',
                     'batchee_harmony = batcher.harmony.cli:main']}

setup_kwargs = {
    'name': 'batchee',
    'version': '1.0.0',
    'description': 'Determine how to group together input files into batches for subsequent concatenation',
    'long_description': '<p align="center">\n    <img alt="batchee, a python package for grouping together filenames to enable subsequent batched operations (such as concatenation)."\n    src="https://github.com/danielfromearth/batchee/assets/114174502/8b1a92a5-eccc-4674-9c00-3698e752077e" width="250"\n    />\n</p>\n\n<p align="center">\n    <a href="https://www.repostatus.org/#active" target="_blank">\n        <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active – The project has reached a stable, usable state and is being actively developed">\n    </a>\n    <a href="https://github.com/python/black" target="_blank">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style">\n    </a>\n    <a href="http://mypy-lang.org/" target="_blank">\n        <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Mypy checked">\n    </a>\n</p>\n\n[//]: # (Using deprecated `align="center"` for the logo image and badges above, because of https://stackoverflow.com/a/62383408)\n\n\n# Overview\n_____\n\n_Batchee_ groups together filenames so that further operations (such as concatenation) can be performed separately on each group of files.\n\n## Installing\n_____\n\nFor local development, one can clone the repository and then use poetry or pip from the local directory:\n\n```shell\ngit clone <Repository URL>\n```\n\n###### (Option A) using poetry:\ni) Follow the instructions for installing `poetry` [here](https://python-poetry.org/docs/).\n\nii) Run ```poetry install``` from the repository directory.\n\n###### (Option B) using pip: Run ```pip install .``` from the repository directory.\n\n## Usage\n_____\n\n```shell\nbatchee [file_names ...]\n```\n\n###### Or, If installed using a `poetry` environment:\n```shell\npoetry run batchee [file_names ...]\n```\n\n#### Options\n\n- `-h`, `--help`            show this help message and exit\n- `-v`, `--verbose`  Enable verbose output to stdout; useful for debugging\n\n---\nThis package is NASA Software Release Authorization (SRA) # LAR-20440-1\n',
    'author': 'Daniel Kaufman',
    'author_email': 'daniel.kaufman@nasa.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
