# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from os import path
from setuptools import setup, Command


BASE_DIR = path.dirname(__file__)


class run_test(Command):
    description = "run unittests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        try:
            from unittest import (TestLoader, TextTestRunner, )
        except ImportError:
            try:
                from unittest2 import (TestLoader, TextTestRunner, )
            except ImportError:
                print('You should use the python version above 2.7 or install unittest2.')
                sys.exit(1)
        path_to_tests = path.join('namedparser', 'testsuite')
        testsuites = TestLoader().discover(path.join(BASE_DIR, path_to_tests))
        TextTestRunner(verbosity=1).run(testsuites)


DESCRIPTION = open(
    path.join(BASE_DIR, 'README.md')
).read().strip()

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name='namedparser',
    version='0.0.1-dev',
    author='OGURA_Daiki',
    author_email='8hachibee125@gmail.com',
    url='https://github.com/hachibeeDI/namedparser',
    description='Read name-daemon configuration files like the bind',
    long_description=DESCRIPTION,
    packages=['namedparser', ],
    license="MIT",
    include_package_data=True,
    entry_points='',
    zip_safe=False,
    platforms='any',
    keywords=['bind', 'named', ],
    install_requires=[
        'pyparsing>=2.0.1',
    ],
    cmdclass={'test': run_test},
    classifiers=classifiers,
)
