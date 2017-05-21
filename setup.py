# -*- coding: utf-8 -*-


from io import open
from setuptools import setup, find_packages

try:
   from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
   from distutils.command.build_py import build_py

setup(
    name='CommonCrawlJob',
    description='Extract data from common crawl using elastic map reduce',
    long_description='\n'.join(
        [
            open('README.rst', encoding='utf-8').read(),
        ]
    ),
    author='Qadium Inc',
    license='Apache Software License v2',
    url='https://github.com/qadium-memex/CommonCrawlJob',
    author_email='sang@qadium.com',
    version='0.1.0',
    packages=find_packages(exclude=['*tests']),
    include_package_data=True,
    use_2to3=True,
    zip_safe=True,
    setup_requires=[
        'setuptools_scm',
        "flake8",
    ],
    install_requires=['warc'],
    entry_points={
        'console_scripts': [
            'crawl_index = aws.__main__:main',
        ]
    },
    cmdclass = {'build_py': build_py},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ]
)
