from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='LogGuard',
    version='0.1.0',
    description='A simple Python Logger',
    author='Charilaos Karametos',
    packages=find_packages(),
    install_requires=required
)
