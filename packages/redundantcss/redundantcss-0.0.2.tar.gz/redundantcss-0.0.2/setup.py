from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Identifies redundant CSS classes not used by the templates provided.'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="redundantcss",
    version=VERSION,
    
    author="Josh Hofer",
    author_email="<josh@securesap.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['beautifulsoup4'],
    keywords=['python', 'css', 'html', 'redundantcss', 'remove unused css'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
      'console_scripts': [
        'redundantcss=redundantcss.redundantcss:main',
      ],
    },
)