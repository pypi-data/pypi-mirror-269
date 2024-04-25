# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pailettes']

package_data = \
{'': ['*']}

install_requires = \
['openai>=1.14.3,<2.0.0', 'rich>=13.7.1,<14.0.0', 'typer[all]>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['pailettes = pailettes.main:app']}

setup_kwargs = {
    'name': 'pailettes',
    'version': '0.1.4',
    'description': 'Generate color palettes using artificial intelligence (OpenAI).',
    'long_description': '# Pailettes\n\nGenerate color palettes using artificial intelligence. The OpenAI API is used for this, so you will require an account.\n\n![Pailettes](https://raw.githubusercontent.com/psyonara/pailettes/master/imgs/headline.jpg)\n\n## Installation\n\n### Pipx\n\n```shell\npipx install pailettes\n```\n\n### Pip\n\n```shell\npip install pailettes\n```\n\n## Configuration\n\nTo configure your OpenAI API key, create an environment variable as follows.\n\n### Linux\n```shell\nexport OPENAI_KEY="your-key-goes-here"\n```\n\n### Windows\nTODO\n\n### MacOS\nTODO\n\nThis will set your OpenAI key for that terminal session. If you would like to permanently set the environment variable, consult the documentation of your OS/shell.\n\n## Usage\n\n### Quick Start\n\n```shell\npailettes retro\n```\n\nThis creates a color palette with a "retro" theme.\n\n### Number of colors\n\nTo specify the number of colors in your palette:\n\n```shell\npailettes retro --color-count=6\n```\n\n### Number of palettes\n\nTo specify the number of palettes to generate:\n\n```shell\npailettes retro --palette-count=3\n```\n\n### Output to JSON\n\nTo output the palettes in JSON format, use the `to-json` parameter:\n\n```shell\npailettes synthwave --palette-count=2 --to-json\n```\n\nAnd to output the JSON to a file, just add the `json-file` parameter:\n\n```shell\npailettes synthwave --palette-count=2 --to-json --json-file=palettes.json\n```\n\nAn example output:\n\n```json\n[\n    {\n        "name": "Neon Sunset",\n        "colors": [\n            "#FF0066",\n            "#FF9900",\n            "#FFCC00",\n            "#33CCFF"\n        ]\n    },\n    {\n        "name": "Digital Dusk",\n        "colors": [\n            "#6600FF",\n            "#00FFCC",\n            "#FF33FF",\n            "#FF6600"\n        ]\n    }\n]\n```\n',
    'author': 'Helmut Irle',
    'author_email': 'me@helmut.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/psyonara/pailettes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
