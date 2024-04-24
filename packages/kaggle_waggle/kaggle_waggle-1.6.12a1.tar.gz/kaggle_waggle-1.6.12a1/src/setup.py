# coding=utf-8
from setuptools import setup, find_packages

# Note: pyproject.toml seems to be chosen by pip install over setup.py, so this
# file is likely not being used anymore. We should verify and merge this into
# pyproject.toml instead of maintaining both flows.
setup(
    name='kaggle_waggle',
    version='1.6.12.a1',
    description='Kaggle API',
    long_description=
    ('Kaggle Waggle API (for https://www.kaggle.com), forked to be used in a Python script primarily.'
     'eta release - Kaggle reserves the right to '
     'modify the API functionality currently offered.'),
    author='Kaggle',
    author_email='support@kaggle.com',
    url='https://github.com/dmitry-v-vlasov/waggle-api',
    project_urls={
        'Documentation': 'https://www.kaggle.com/docs/api',
        'GitHub': 'https://github.com/dmitry-v-vlasov/waggle-api',
        'Tracker': 'https://github.com/dmitry-v-vlasov/waggle-api/issues',
    },
    keywords=['Kaggle', 'Waggle', 'API'],
    entry_points={'console_scripts': ['kaggle = kaggle.cli:main']},
    install_requires=[
        'six >= 1.10',
        'certifi >= 2023.7.22',
        'python-dateutil',
        'requests',
        'tqdm',
        'python-slugify',
        'urllib3',
        'bleach',
    ],
    packages=find_packages(exclude=("src.*", "src")),
    license='Apache 2.0')
