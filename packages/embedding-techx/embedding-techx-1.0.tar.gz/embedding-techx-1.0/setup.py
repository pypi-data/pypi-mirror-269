from setuptools import setup, find_packages

setup(
    name = 'embedding-techx',
    package = ['embedding-techx'],
    version = '1.0',
    install_requires = [
        'sentence-transformers',
        'torch',
        'pandas',
        'IPython',
        'langdetect',
        'pycountry',
        'time',
        'sklearn',
        'seaborn',
        'matplotlib',
    ],
    packages = find_packages()
)