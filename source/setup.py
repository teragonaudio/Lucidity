from distutils.core import setup
from distutils.extension import Extension
import sys

setup(name = "lucidity",
      packages = ['lucidity'],
      author = "Teragon Audio",
      package_dir = {'lucidity': 'lucidity'},
      package_data = {'lucidity': ["*.sql", "*/*.py"]},
)
