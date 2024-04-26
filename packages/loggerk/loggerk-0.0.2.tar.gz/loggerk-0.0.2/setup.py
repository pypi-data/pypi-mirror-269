import pathlib

from setuptools import setup, find_packages

here: pathlib.Path = pathlib.Path(__file__).parent.resolve()

long_description: str = (here / "README.md").read_text(encoding="utf-8")

VERSION = "0.0.2"
DESCRIPTION = "This is a custom logger module for Python"

# Setting up
setup(
    name="loggerk",
    version=VERSION,
    author="Kuantik DataJump",
    author_email="master@kuantik.mx",
    maintainer="Angel de Jesús Sanchez Morales",
    maintainer_email="angel.sanchez@kuantik.mx",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["httpx"],
    keywords=["python", "logging"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
