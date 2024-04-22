from setuptools import setup, find_packages



setup(
    name='LogGuard',
    version='0.2.1',
    description='A simple Python Logger',
    author='Charilaos Karametos',
    packages=find_packages(),
    install_requires=[
        "astroid==3.1.0",
        "colorama==0.4.6",
        "dill==0.3.8",
        "flake8==7.0.0",
        "flake8-commas==2.1.0",
        "flake8-docstrings==1.7.0",
        "isort==5.13.2",
        "mccabe==0.7.0",
        "pathlib==1.0.1",
        "platformdirs==4.2.0",
        "pycodestyle==2.11.1",
        "pydocstyle==6.3.0",
        "pyflakes==3.2.0",
        "pylint==3.1.0",
        "snowballstemmer==2.2.0",
        "tomlkit==0.12.4"
        ],
    package_data={'': ['log_settings.json']},  # Include log_settings.json as package data
)
