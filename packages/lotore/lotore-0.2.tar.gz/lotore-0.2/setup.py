from setuptools import setup, find_packages

setup(
    name="lotore",
    version="0.2",
    packages=find_packages(),
    long_description=open('README.md', 'r').read(),
    entry_points={
        "console_scripts": [
            "lotore = lotore:description"
        ],
    },
)