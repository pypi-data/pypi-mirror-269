#!/usr/bin/env python3
from setuptools import setup


def get_version():
    return 7 #import subprocess
    cmd = ['git', 'rev-list', 'HEAD', '--count']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    rev = int(stdout)
    return u'%s' % rev


setup(
    name="mdrocr",
    version="%s" % get_version(),
    description="multi directory recursive ocr images and turn into pdfs",
    author="j",
    author_email="j@mailb.org",
    url="https://r-w-x.org/r/mdrocr",
    license="GPLv3",
    scripts=[
        'mdrocr',
    ],
    install_requires=[
    ],
    keywords=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
)
