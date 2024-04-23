'''
Description: aka.zhp
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-04 21:12:45
LastEditTime: 2024-04-23 10:16:11
'''
import setuptools
import os, shutil
from distutils.core import setup
from nlpknife import __version__ as version

with open("./requirements.txt", "r") as f:
    install_requires = f.read().splitlines()
print(install_requires)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="nlpknife",
    version=version,
    author="zhpmatrix",
    description="my nlpknife",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/zhpmatrix/nlpknife",
    packages=setuptools.find_packages(exclude=["test"]),
    download_url="https://pypi.tuna.tsinghua.edu.cn/simple",
    python_requires=">=3.7",
    install_requires=install_requires,
    package_data={
        '': ['*.yaml', '*.json', "*.csv", "*.txt", "*.json", "*.pkl"],
    }
)
