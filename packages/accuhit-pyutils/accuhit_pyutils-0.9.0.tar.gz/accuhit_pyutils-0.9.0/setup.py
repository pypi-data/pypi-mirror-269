# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup, __version__

install_requires = [
    "pytz==2024.1",
    "pandas>=0.23.4",
    "boto3~=1.34.74",
    "botocore~=1.34.74",
    "python-dateutil==2.9.0.post0",
    "Werkzeug>=0.14.1",
    "pymongo~=4.6.2"
]


def read(fname):
    """Utility function to read the README file into the long_description."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


version_file = "version.py"
with open(version_file) as fp:
    exec(fp.read())

setup(
    name="accuhit-pyutils",
    version=__version__,
    author="accuhit",
    author_email="developer@accuhit.net",
    description="accuhit deeplearning library",
    license="Copyright accuhit",
    py_modules=['accuhit-pyutils'],
    install_requires=install_requires,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.11',
    ]
)
