from setuptools import setup

setup_args = {
    'zip_safe': False,
    'author': "Mark Nunberg",
    'author_email': "mnunberg@haskalah.org",
    'license': "Apache License 2.0",
    'description': "Couchbase Client API using CFFI",
    'keywords': ["PyPy", "nosql", "pycouchbase", "libcouchbase", "couchbase"],
    'install_requires': ['cffi', 'couchbase'],
    'tests_require': ['nose', 'testresources'],

    'classifiers': [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython"
    ],

    'packages': ['couchbase_ffi'],
    'package_data': {'couchbase_ffi':['_lcb.h']},
    'name': 'couchbase_ffi',
    'version': '0.1.0',
    'url': 'https://github.com/couchbaselabs/couchbase-python-cffi'
}

setup(**setup_args)
