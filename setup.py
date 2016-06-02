try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'affirm',
    'author': 'Eli Finer',
    'author_email': 'eli.finer@gmail.com',
    'version': '0.9',
    'py_modules': ['affirm'],
    'description': '''\
Improved error messages for Python assert statements.
See: http://github.com/gooli/affirm
'''
}

setup(**config)
