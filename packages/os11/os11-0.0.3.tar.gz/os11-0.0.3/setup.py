from setuptools import setup, find_packages;
import codecs;
import os;

VERSION = '0.0.3'
DESCRIPTION = 'os11'
LONG_DESCRIPTION = 'A package to perform details of os programs'

# Setting up
setup(
    name="os11",
    version=VERSION,
    author="KTHM",
    author_email="kthmcollegenashik1@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'os', 'college', 'python tutorial', 'os college'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)