"""
    This library is meant to be a module-based technical analysis library.
"""
import pathlib
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="technical-analysis",
    version="2023.5.7.4",
    description="A simple, generic Python technical analysis library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruin2121/technical-analysis",
    author="Ruin2121",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="technical analysis",
    packages=find_packages(),
    python_requires=">=3.10.9, <4",
)
