from os import path
from setuptools import setup

DESCRIPTION = open(
    path.join(path.dirname(__file__), 'README.md')
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
    classifiers=classifiers,
)
