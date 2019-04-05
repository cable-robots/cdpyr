#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

NAME = "cdpyr"
AUTHOR = "Philipp Tempel"
EMAIL = "philipp.tempel@isw.uni-stuttgart.de"
KEYWORDS = "cdpyr cable-driven parallel robot"

VERSION = None

# The rest you shouldn't have to touch too much :)


here = os.path.abspath(os.path.dirname(__file__))

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('LICENSE') as license_file:
    LICENSE = license_file.read()

parsed_requirements = parse_requirements(
    'requirements/prod.txt',
    session=PipSession()
)

parsed_test_requirements = parse_requirements(
    'requirements/test.txt',
    session=PipSession()
)

requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__init__.py')) as f:
        ls = [l.strip() for l in f.readlines()]
        try:
            about['__version__'] = [v for v in ls if '__version__' in v][0].split(' = ')[1].strip('\'')
        except IndexError:
            about['__version__'] = VERSION
else:
    about['__version__'] = VERSION

setup(
    author=AUTHOR,
    author_email=EMAIL,
    description="Cable-Driven Parallel Robots in Python.",
    entry_points={
        'console_scripts': [
            'cdpyr=cdpyr.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords=KEYWORDS,
    name=NAME,
    license=LICENSE,
    packages=find_packages(include=['cdpyr']),
    # setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://www.cable-robots.com/cdpyr/',
    version=about['__version__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
)
