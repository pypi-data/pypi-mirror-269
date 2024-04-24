from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.9'
DESCRIPTION = 'python optimization'
LONG_DESCRIPTION = 'A package that allows python optimization'

# Setting up
setup(
    name="python_optimization",
    version=VERSION,
    author="founder synergy",
    author_email="founders.synergy@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)