from setuptools import setup, find_packages

import pathlib
__version__ = "1.0.2"

setup(
    name="qdataclass",
    version=__version__,
    author="林柏君",
    author_email="1355767057@qq.com",
    description="自动生成QProperty的getter setter notify",
    packages=find_packages()
)
