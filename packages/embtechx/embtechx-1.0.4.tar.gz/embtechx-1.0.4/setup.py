from setuptools import setup, find_packages

setup(
    name = 'embtechx',
    package = ['embtechx'],
    version = '1.0.4',
    install_requires = [
        'sentence-transformers',
        'torch',
        'pandas',
        'IPython',
        'langdetect',
        'scikit-learn',
        'seaborn',
        'matplotlib',
    ],
    packages = find_packages()
)