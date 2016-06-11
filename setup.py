try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'affirm',
    'url': 'https://github.com/gooli/affirm',
    'author': 'Eli Finer',
    'author_email': 'eli.finer@gmail.com',
    'version': '0.9.2',
    'py_modules': ['affirm'],
    'description': 'Improved error messages for Python assert statements'
}

setup(**config)
