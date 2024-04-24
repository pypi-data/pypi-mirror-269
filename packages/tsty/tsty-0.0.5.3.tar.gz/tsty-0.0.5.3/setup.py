from setuptools import setup, find_packages
import os

VERSION = "0.0.5.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

setup(
    name="tsty",
    description="A simple command-line utility for changing your terminal colors",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Dan Nguyen",
    url="https://github.com/dannguyen/tsty",
    project_urls={
        "Issues": "https://github.dannguyen/dannguyen/tsty/issues",
        "CI": "https://github.com/dannguyen/tsty/actions",
        "Changelog": "https://github.com/dannguyen/tsty/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=find_packages(exclude=["tests", "tests.*"]),
    entry_points="""
        [console_scripts]
        tsty=tsty.cli:cli
    """,
    install_requires=[
        "click>=8.1",
        "click-default-group>=1.2.3",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-mock",
            "black>=24.2.0",
            "types-click",
        ]
    },
    python_requires=">=3.8",
)
