import os
from setuptools import setup, find_packages


def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name="py-hmh",
    version="0.1",
    author="Animesh Pandey",
    author_email="apanimesh061@gmail.com",
    license="Apache License 2.0",
    url="",
    keywords="hmh api",
    description="A Python wrapper around the HMH Developer Portal API",
    long_description=(read("readme.rst") + "\n\n" + read("authors.rst") + "\n\n" + read("CHANGES")),
    packages=find_packages(exclude=["tests*"]),
    install_requires=["poster"]
)
