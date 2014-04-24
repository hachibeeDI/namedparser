# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import sys
from os import path
from setuptools import setup, Command


BASE_DIR = path.dirname(__file__)

IS_OLD_PYTHON2 = sys.version_info[1] in [5, 6]


class run_test(Command):
    description = "run unittests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from unittest import (TestLoader, TextTestRunner, )
        if IS_OLD_PYTHON2:
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


REQUIRE_MODULES = open('requirements.txt').read().splitlines()
if IS_OLD_PYTHON2:
    REQUIRE_MODULES.append('unittest2')

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
    install_requires=REQUIRE_MODULES,
    cmdclass={'test': run_test},
    classifiers=classifiers,
)
