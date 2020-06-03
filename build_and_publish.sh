#!/bin/bash
rm -rf ./airthings.egg-info/ ./dist/ ./build/
python setup.py sdist bdist_wheel
twine upload --repository testpypi dist/*

