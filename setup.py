#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='aims',
    version='0.1',
    description='Aid Information Management System',
    long_description=open('README.md', 'r').read(),
    packages=['aims', 'myanmar', 'profiles', ],
    package_data={'aims': ['templates/*.html',
                          'templates/aims/*',
                          'templates/registration/*'
                          'static/css/images/*',
                          'static/css/*.css',
                          'static/js/*',
                          'static/images/*',
                          'static/geo/*'],
                  'myanmar': [
                      'data/1_adm0_country_250k_mimu/*',
                      'data/2_adm1_states_regions1_250k_mimu/*',
                      'data/4_adm2_districts_250k_mimu/*',
                      'data/5_adm3_townships1_250k_mimu/*'
                  ]},
    install_requires=['Django==1.6'],
    zip_safe=False,
    requires=[],
    classifiers=[
      'Environment :: Web Environment',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Internet :: WWW/HTTP',
      'Topic :: Software Development :: Libraries',
    ],
)
