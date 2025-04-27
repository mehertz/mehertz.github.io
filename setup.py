"""
This setup.py file is maintained for backward compatibility.
For new installations, we recommend using uv with pyproject.toml.

See the README.md for instructions on using uv for reproducible builds.
"""

from setuptools import setup, find_packages

setup(
    name="ssg",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jinja2",
        "markdown",
        "python-frontmatter",
    ],
    entry_points={
        "console_scripts": [
            "ssg=ssg.cli:main",
        ],
    },
) 