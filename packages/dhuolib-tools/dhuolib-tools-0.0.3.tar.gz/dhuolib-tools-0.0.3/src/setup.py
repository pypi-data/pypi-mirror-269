# https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
import os
from setuptools import setup, find_packages


REQUIRED_PACKAGES = open("requirements.txt").readlines()

DEV_PACKAGES = []
if os.path.exists("requirements.dev.txt"):
    DEV_PACKAGES = open("requirements.dev.txt").readlines()

README = ""
if os.path.exists("README.md"):
    README = open("README.md").read()

setup(
    name="dhuolib",
    version="0.0.1",
    long_description=README,
    long_description_content_type="text/markdown",
    author="DHuO Data Team",
    author_email="dhuodata@engdb.com.br",
    url="https://gitlab.engdb.com.br/dhuo-plat/dhuo-data/data-science/dhuolib",
    install_requires=REQUIRED_PACKAGES,
    extras_require={"interactive": DEV_PACKAGES},
    packages=find_packages(include=["src", "src.*"]),
    platforms="any",
)
