#!/bin/bash
#first time you have to run python3 setup.py register

version=$((`git rev-list HEAD --count`))
sed -i "s/import subprocess/return $version #import subprocess/g" setup.py
python3 setup.py sdist
twine upload dist/mdrocr-${version}.tar.gz
sed -i "s/return $version #//g" setup.py

