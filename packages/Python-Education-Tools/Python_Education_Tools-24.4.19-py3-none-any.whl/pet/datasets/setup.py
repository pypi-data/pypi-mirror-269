
from setuptools import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize("factory.py", language_level=3))
