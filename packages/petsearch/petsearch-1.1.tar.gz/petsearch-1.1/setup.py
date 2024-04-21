# setup.py

from setuptools import setup, find_packages

setup(
    name='petsearch',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your library requires
        'Django>=3.0',  # Example dependency
    ],
    author='x23202513student',
    author_email='x23202513@student.ncirl.ie',
    description='A library for searching pets',
)
