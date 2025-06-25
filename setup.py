"""
Setup configuration for PyHetznerServer.

This setup.py is maintained for backward compatibility.
The main configuration is now in pyproject.toml.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="pyhetznerserver",
    version="1.2.0",
    author="Mohammad Rasol Esfandiari",
    author_email="mrasolesfandiari@gmail.com",
    description="A modern, type-safe Python library for Hetzner Cloud Server management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeepPythonist/PyHetznerServer",
    project_urls={
        "Bug Tracker": "https://github.com/DeepPythonist/PyHetznerServer/issues",
        "Documentation": "https://pyhetznerserver.readthedocs.io/",
        "Source Code": "https://github.com/DeepPythonist/PyHetznerServer",
        "Changelog": "https://github.com/DeepPythonist/PyHetznerServer/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0"
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.19.0"
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.22.0"
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    keywords=[
        "hetzner", "cloud", "server", "api", "management", 
        "infrastructure", "hosting", "vps"
    ],
    license="MIT",
    zip_safe=False,
) 