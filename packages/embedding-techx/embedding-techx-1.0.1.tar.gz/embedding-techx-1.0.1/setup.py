from setuptools import setup, find_packages

setup(
    name = 'embedding-techx',
    package = ['embedding-techx'],
    version = '1.0.1',
    install_requires = [
        'sentence-transformers',
        'torch',
        'pandas',
        'IPython',
        'langdetect',
        'sklearn',
        'seaborn',
        'matplotlib',
    ],
    packages = find_packages()
)