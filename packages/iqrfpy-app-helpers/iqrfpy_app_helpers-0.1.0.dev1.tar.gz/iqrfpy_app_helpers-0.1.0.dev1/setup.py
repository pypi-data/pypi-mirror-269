from __future__ import annotations
from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='iqrfpy-app-helpers',
    description='Diagnostics for iqrfpy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0-dev1',
    url='https://gitlab.iqrf.org/open-source/iqrf-sdk/iqrfpy/iqrfpy-app-helpers',
    author='Karel Hanák',
    author_email='karel.hanak@iqrf.org',
    license='Apache-2.0',
    keywords=['iqrf'],
    project_urls={
        'Homepage': 'https://gitlab.iqrf.org/open-source/iqrf-sdk/iqrfpy/iqrfpy-app-helpers',
        'Changelog': 'https://gitlab.iqrf.org/open-source/iqrf-sdk/iqrfpy/iqrfpy-app-helpers/-/blob/master/changelog.md',
        'Source code': 'https://gitlab.iqrf.org/open-source/iqrf-sdk/iqrfpy/iqrfpy-app-helpers',
        'Issue tracker': 'https://gitlab.iqrf.org/open-source/iqrf-sdk/iqrfpy/iqrfpy-app-helpers/-/issues',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    packages=['iqrfpy.ext.app_helpers'],
    package_dir={
        'iqrfpy.ext.app_helpers': 'app_helpers'
    },
    package_data={
        'iqrfpy.ext.app_helpers': [
            'py.typed'
        ]
    },
    python_requires='>=3.10',
    install_requires=[
        'iqrfpy>=0.2.0',
        'tabulate>=0.9.0',
    ]
)
