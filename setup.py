import os
import sys
from setuptools import setup

PKG = "ubiquerg"
REQDIR = "requirements"


def read_reqs(reqs_name):
    depsfile = os.path.join(REQDIR, "requirements-{}.txt".format(reqs_name))
    with open(depsfile, "r") as f:
        return [l.strip() for l in f if l.strip()]


with open(os.path.join(PKG, "_version.py"), "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

with open("README.md") as f:
    long_description = f.read()
    
setup(
    name=PKG,
    packages=[PKG],
    version=version,
    description="Various utility functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="utility, utilities, tools",
    url="https://github.com/pepkit/{}/".format(PKG),
    author=u"Vince Reuter",
    license="BSD-2-Clause",
    scripts=None,
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
)
