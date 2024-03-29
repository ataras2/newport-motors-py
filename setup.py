import setuptools
import os
import codecs
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

# long_description = "A python package for operating multiple newport motors in an optical setup"

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# DEPENDENCIES
# 1. What are the required dependencies?
# with open("requirements.txt") as f:
#     install_requires = f.read().splitlines()
# 2. What dependencies required to run the unit tests? (i.e. `pytest --remote-data`)
# tests_require = ['pytest', 'pytest-cov', 'pytest-remotedata']


setuptools.setup(
    name="newport-motors-py",
    version=find_version("newport_motors", "__init__.py"),
    description="A python package for operating newport motors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adam Taras",
    author_email="adam.taras@sydney.edu.au",
    url="https://github.com/ataras2/newport_motors",
    project_urls={
        "Bug Tracker": "https://github.com/ataras2/newport_motors/issues",
    },
    # package_dir={"": "src"},
    packages=[
        "newport_motors",
        "newport_motors/GUI",
        "newport_motors/Motors",
        "newport_motors/Mocks",
        "newport_motors/USBs",
        "pyvisa_mock",
    ],
    install_requires=[
        "pytest==7.3.1",
        "streamlit==1.22.0",
        "usbinfo==1.1.2",
        "PyVISA==1.13.0",
        "PyVISA-py==0.6.3",
        "PyYAML==6.0",
        "parse==1.19.0",
        "visa==1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # packages = ["src"] + setuptools.find_namespace_packages(where = "src")
)
