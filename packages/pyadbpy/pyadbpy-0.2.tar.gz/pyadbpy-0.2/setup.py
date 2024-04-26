# setup.py

from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='pyadbpy',
    version='0.2',
    packages=find_packages(),
    author='termuxdev314',
    author_email='termuxdev314@gmail.com',
    description='Ein Modul für ADB Operationen.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/termuxdev314/adbpy',
    install_requires=[
        # Hier kannst du benötigte Pakete hinzufügen
    ],
)
