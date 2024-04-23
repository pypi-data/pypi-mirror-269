import glob
from os import path
from setuptools import find_packages, setup

local = path.abspath(path.dirname(__file__))

with open(path.join(local, "readme.md"), "r", encoding="utf-8") as f:
    long_description = f.read()


class FilePicker:
    def __init__(self):
        pass

    def sql_file_picker(self):
        sql_files = []
        directories = glob.glob(path.join(local, "/showroom\\**\\"))
        for directory in directories:
            files = glob.glob(directory + "*.sql")
            if len(files) != 0:
                sql_files.append((directory, files))
        return sql_files


setup(
    name="showroom",
    version="0.1",
    description="Ntt Showroom models and schemas",
    data_files=FilePicker().sql_file_picker(),
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Ntt Backend Team",
    author_email="lucassilluzio@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    keywords="package ntt development",
    install_requires=[
        "PyMySQL==1.1.0",
        "SQLAlchemy==2.0.28",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
