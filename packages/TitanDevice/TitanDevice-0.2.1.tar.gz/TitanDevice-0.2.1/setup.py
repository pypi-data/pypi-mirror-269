import setuptools
from setuptools import setup
import os


# Read the content of `README.md`:
def read_readme():
    with open(os.path.join(os.getcwd(), 'README.md'), 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name="TitanDevice",
    version="0.2.1",
    author="369",
    author_email="luck.yangbo@gmai.com",
    description="A Python library used for managing device",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'adbutils',
        'pydantic'
    ],
)
