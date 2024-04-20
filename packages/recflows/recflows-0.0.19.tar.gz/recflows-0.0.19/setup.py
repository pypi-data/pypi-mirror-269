from setuptools import setup, find_packages
import os


def read(name):
    with open(name) as f:
        return f.read()


def read_requirements():
    return read('requirements.txt').splitlines()


setup(
    name="recflows",
    version=os.environ.get("RECFLOWS_VERSION"),
    description="Solution created to streamline the creation, programming, deployment and monitoring of recommendation systems.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/cogdiver/recflows",
    license="MIT",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="cogdiver",
    keywords=[
        "recommendation systems",
        "programming"
    ],
)