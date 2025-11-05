"""
Setup Script
This script sets up the ORM framework as a Python package.
"""

from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="custom-orm-framework",
    version="1.0.0",
    author="Python Learning Series",
    author_email="example@example.com",
    description="A custom Object-Relational Mapping framework built from scratch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/python-learning-series/custom-orm-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies are part of Python standard library
        # sqlite3
        # json
        # threading
        # contextlib
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "extended": [
            # Optional dependencies for extended functionality
            # "psycopg2>=2.9.0",  # PostgreSQL
            # "PyMySQL>=1.0.0",   # MySQL
            # "sqlalchemy>=1.4.0", # Connection pooling
        ],
    },
    entry_points={
        "console_scripts": [
            "orm-demo=examples.basic_usage:main",
        ],
    },
)