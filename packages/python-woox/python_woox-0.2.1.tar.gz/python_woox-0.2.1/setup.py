from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="python-woox",
    version="0.2.1",
    author="tinghsuwan",
    author_email="wanth1997@gmail.com",
    description="WooX python API",
    license="MIT",
    url="https://github.com/wanth1997/python-wootrade",
    packages=["woox"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "aiohttp", "websockets"],
    zip_safe=True,
)
