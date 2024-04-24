from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='libsmartocr',
    version='0.1.0',
    author='Kogui',
    description='Uma lib de conexão de testt',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lucasaarrudaa/lib-repo-test',  
    packages=find_packages(),
    install_requires=[
        'pyodbc',
    ],
    python_requires='>=3.6',  
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)