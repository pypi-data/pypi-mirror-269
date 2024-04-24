from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Simplify RPA activities with a browser.'
LONG_DESCRIPTION = 'A package that allows to execute RPA activities without configuration'

# Setting up
setup(
    name="pyrpabrowserdemo",
    version=VERSION,
    author="Daniel Rubens",
    author_email="danielrubensdaniel@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'rpaframework==28.5.1'],
    keywords=['python', 'rpa', 'robocorp', 'pdf', 'html', 'conversor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)