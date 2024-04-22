from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name='rconnet',
  version='0.0.2',
  author='VordyV',
  author_email='vordy.production@gmail.com',
  description='Python RCON client for the Battlefield 2142 server',
  #long_description=long_description,
  url='https://github.com/VordyV/rconnet',
  packages=find_packages(),
  keywords='rcon client',
  python_requires='>=3.11'
)