from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="basic-bar",
    version="0.4",
    description="A simple and efficient progress bar",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Spencer Churchill",
    author_email="spence@duck.com",
    url="https://github.com/splch/py-basic-bar",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
    ],
)
