from setuptools import setup, find_packages

setup(
    name='eReuse-DeviceHub',
    version='0.4',
    packages=find_packages(exclude=('contrib', 'docs', 'scripts')),
    url='https://github.com/eReuse/DeviceHub',
    license='AGPLv3 License',
    author='eReuse.org team',
    author_email='x.bustamante@ereuse.org',
    description='DeviceHub is a system to manage devices focused in reusing them. ',
    # Updated in 2017-07-29
    install_requires=[
        'inflection>=0.3.1',
        'eve>=0.6.3,<0.8',
        'werkzeug>=0.9.4,<=0.11.15',
        'flask>=0.11,<0.12',  # eve < 0.8 breaks with flask 0.12
        'passlib>=1.6.5,<2.0',
        'validators>=0.10,<0.20',
        'requests>=2.9.1,<3.0',
        'python-gnupg>=0.3.8',  # To use gnupg, install gpg2
        # Superior versions have a version mismatch of werkzeug with eve
        # Only update flask-caching when updating eve to >=0.8
        'flask-caching<=1.2.0',
        'python-gnupg',
        'iso3166',
        'flask-excel>=0.0.7,<0.0.8',
        'pyexcel-ods',
        'pyexcel-xlsx',
        'pydash>=4.0,<5.0',
        'sortedcontainers>=1.5.7,<1.6',
        'geojson_utils',
        'geojson>=1.3.4,<1.4',
        'geoip2>=2.4.2,<3',
        'flask-cors>=3.0.2,<4',
        'shortid>=0.1.2,<0.2',
        'beautifulsoup4>=4.6,<5',
        'wikipedia>=1.4,<2',
        'Flask-WeasyPrint',
        'toolz>=0.8,<1.0',
        'geojson_utils'
    ],
    keywords='eReuse.org DeviceHub devices devicehub reuse recycle it asset management',
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
    # Install it with pip install .[docs] or pip install -e .[docs]
    extras_require={
        'docs': [
            'sphinx>=1.4.7',
            'sphinxcontrib-httpdomain>=1.5'
        ]
    },
    # Use `python setup.py test` to run the tests
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite
    test_suite='ereuse_devicehub.tests',
    tests_require=[
        'assertpy'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
