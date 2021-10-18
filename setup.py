from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'A basic web scrapper package.'

# Setting up
setup(
    name="scraper",
    version=VERSION,
    author="Mugesh Kannan",
    author_email="<mugeshk1171@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests', 'tqdm'],
    keywords=['python', 'google', 'web scrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
