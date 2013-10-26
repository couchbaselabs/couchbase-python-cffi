#!/bin/sh
set -e
set -x
git clone git://github.com/mnunberg/couchbase-python-client
cd couchbase-python-client
sudo $(which python) setup.py install
cp .tests.ini.travis ../tests.ini
