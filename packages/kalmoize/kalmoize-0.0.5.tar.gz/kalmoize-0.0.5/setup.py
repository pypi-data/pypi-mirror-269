#!/usr/bin/env python


from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from kalmoize import __version__
setup(name='kalmoize',
    version=__version__,
    packages=['kalmoize'],
    description='Rock solid memoize for Python/Tornado',
    author='Piotr Czesław Kalmus',
    author_email='pckalmus@gmail.com',
    url='https://github.com/pekoslaw/kalmoize',
    keywords = ['memcache', 'cache', 'tornado'],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Natural Language :: Polish",
        #"Framework :: Tornado",
        "Environment :: Web Environment",
        "Environment :: Other Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Other/Nonlisted Topic",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        
    ],
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("kalmoize.utils", ["kalmoize/utils.py"]),
                   Extension("kalmoize.decorators", ["kalmoize/decorators.py"]),
                   ]
)