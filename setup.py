# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import sys
from os import path

from setuptools import setup, Command


BASE_DIR = path.dirname(__file__)

IS_OLD_PYTHON2 = sys.version_info[1] in [5, 6]
REQUIRE_MODULES = open('_requirements.txt').read().splitlines()
if IS_OLD_PYTHON2:
    REQUIRE_MODULES.append('unittest2')


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


# to suppres verbosity logging message of distutils

def run_command(self, command):
    if self.have_run.get(command):
        return
    cmd_obj = self.get_command_obj(command)
    cmd_obj.ensure_finalized()
    cmd_obj.run()
    self.have_run[command] = 1
from distutils.dist import Distribution
Distribution.run_command = run_command


class show_require_modules(Command):
    description = "show require modules"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for r in REQUIRE_MODULES:
            print(r)


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
    version='0.0.1',
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
    cmdclass={
        'test': run_test,
        'requires': show_require_modules,
    },
    classifiers=classifiers,
)
