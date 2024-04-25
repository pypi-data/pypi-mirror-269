from os import path
from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cli-fragments",
    version="1.2.0",
    author="Luca Saladino",
    author_email="sal65535@protonmail.com",
    description="Awesome CLI input and output functions for Python 3.x scripts.",
    packages=["cli_fragments"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
