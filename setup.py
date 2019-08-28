from distribute_setup import use_setuptools
use_setuptools()

import sys
from setuptools import setup


import telenor_web2sms


if sys.version_info < (2, 6):
    print 'ERROR: telenor_web2sms requires at least Python 2.6 to run.'
    sys.exit(1)


setup(
    name='telenor_web2sms',
    version=telenor_web2sms.__version__,
    url='https://github.com/petarmaric/telenor_web2sms',
    download_url='https://github.com/petarmaric/telenor_web2sms',
    license='BSD',
    author='Petar Maric',
    author_email='petar.maric@gmail.com',
    description='Console app and Python API for sending SMSs through the Telenor WEB2SMS web app',
    long_description=open('README').read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Communications',
        'Topic :: Utilities',
    ],
    platforms='any',
    py_modules=['telenor_web2sms'],
    entry_points={
        'console_scripts': ['telenor_web2sms=telenor_web2sms:main']
    },
    install_requires=open('requirements.txt').read().splitlines(),
)
