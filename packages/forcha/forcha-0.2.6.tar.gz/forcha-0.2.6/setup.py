# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forcha',
 'forcha.components.archiver',
 'forcha.components.evaluator',
 'forcha.components.evaluator.parallel',
 'forcha.components.nodes',
 'forcha.components.orchestrator',
 'forcha.components.settings',
 'forcha.exceptions',
 'forcha.models',
 'forcha.models.templates',
 'forcha.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=1.0.1',
 'matplotlib>=3.7.1',
 'numpy>=1.26.0',
 'scikit-learn>=1.2.0',
 'timm>=0.9',
 'torch>=2.0.0',
 'torchaudio>=2.0.2',
 'torchvision>=0.15.1']

setup_kwargs = {
    'name': 'forcha',
    'version': '0.2.6',
    'description': '',
    'long_description': '',
    'author': 'Maciej Zuziak',
    'author_email': 'maciejkrzysztof.zuziak@isti.cnr.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Scolpe/forcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.09,<4.0',
}


setup(**setup_kwargs)
