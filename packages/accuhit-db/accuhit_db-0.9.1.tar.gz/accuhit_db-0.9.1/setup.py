# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup, __version__


def read(fname):
    """Utility function to read the README file into the long_description."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


version_file = "version.py"
with open(version_file) as fp:
    exec(fp.read())

setup(
    name="accuhit-db",
    version=__version__,
    author="accuhit",
    author_email="developer@accuhit.ai",
    description="accuhit database common library",
    license="Copyright accuhit",
    py_modules=['accuhit-db'],
    # zip_safe=False,
    platforms='ubuntu, MacOS, centos',
    install_requires=[
        "pymongo==4.6.3",
        "PyMySQL==1.1.0",
        "pytz>=2018.7",
        "six>=1.11.0",
        "SQLAlchemy~=2.0.29",
        "psycopg2-binary~=2.9.9",
        "certifi~=2024.2.2"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.6.3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(exclude=["test"]),
    include_package_data=True
)
