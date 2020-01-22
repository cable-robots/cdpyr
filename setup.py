#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
        name='cdpyr',
        version='1.0.dev0',
        license='EUPL v1.2',
        description='A Python 3 package for designing, analyzing, '
                    'and simulating cable-driven parallel robots.',
        long_description='%s\n%s' % (
                re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
                    '', read('README.rst')),
                re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
        ),
        author='Philipp Tempel',
        author_email='p.tempel@tudelft.nl',
        url='https://github.com/cable-robots/cdpyr',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        include_package_data=True,
        zip_safe=False,
        classifiers=[
                # complete classifier list:
                # http://pypi.python.org/pypi?%3Aaction=list_classifiers
                'Development Status :: 2 - Pre-Alpha',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: European Union Public Licence 1.2 '
                '(EUPL 1.2)',
                'Operating System :: Unix',
                'Operating System :: POSIX',
                'Operating System :: Microsoft :: Windows',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.7',
                'Topic :: Utilities',
        ],
        project_urls={
                'Documentation': 'https://cdpyr.readthedocs.io/',
                'Changelog':
                    'https://cdpyr.readthedocs.io/en/latest/changelog.html',
                'Issue Tracker': 'https://github.com/cable-robots/cdpyr/issues',
        },
        keywords=[
                # eg: 'keyword1', 'keyword2', 'keyword3',
        ],
        python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, '
                        '!=3.5.*, !=3.6.*',
        install_requires=[
                'click',
                'numpy',
                'scipy',
                'colour',
                'repr',
                'xmltodict',
                'marshmallow',
                'joblib',
                'watchdog',
                'hurry.filesize',
                'tabulate',
                'fastnumbers',
                'cached-property',
                'pint',
                'python-string-utils',
                'more-itertools',
        ],
        extras_require={
                'visualization': [
                        'matplotlib',
                        'plotly',
                        'vtk'
                ],
        },
        entry_points={
                'console_scripts': [
                        'cdpyr = cdpyr.cli:main',
                ]
        },
)
