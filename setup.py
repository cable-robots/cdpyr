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

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
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

parsed_setup_requirements = parse_requirements(
    'requirements/setup.txt',
    session=PipSession()
)

requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]
setup_requirements = [str(tr.req) for tr in parsed_setup_requirements]

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__init__.py')) as f:
        ls = [l.strip() for l in f.readlines()]
        try:
            about['__version__'] = \
                [v for v in ls if '__version__' in v][0].split(' = ')[1].strip(
                    '\'')
        except IndexError:
            about['__version__'] = VERSION
else:
    about['__version__'] = VERSION

setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='A Python 3.7 package for designing, analyzing, and simulating cable-driven parallel robots.',
    entry_points={
        'console_scripts': [
            'cdpyr=cdpyr.cli:main',
        ],
    },
    install_requires=requirements,
    license=LICENSE,
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords=KEYWORDS,
    name=NAME,
    packages=find_packages(include=['cdpyr']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://cable-robot.science/cdpyr',
    version='0.1.0',
    zip_safe=False,
)
