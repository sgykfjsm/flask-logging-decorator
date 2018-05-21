#!/usr/bin/env python
from setuptools import setup
from os.path import abspath, dirname, join
from codecs import open

here = abspath(dirname(__file__))

long_description = ''
with open(join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

extras_require_dev = []
with open(join(here, 'requirement_dev.txt'), encoding='utf-8') as f:
    for line in f.readlines():
        if '==' in line:
            extras_require_dev.append(line.split('==')[0])

setup(
    name='flask_logging_decorator',
    version='0.0.3',
    description='Simple logging decorator for Flask.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sgykfjsm/flask-logging-decorator',
    author='Shigeyuki Fujishima',
    author_email='shigeyuki.fujishima@gmail.com',
    python_requires=">=3.5, !=2.*.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='flask logging decorator',
    py_modules=('flask-logging-decorator',),
    extras_require={'dev': extras_require_dev, },
    packages=['flask_logging_decorator']
    )
