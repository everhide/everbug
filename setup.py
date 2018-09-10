from distutils.core import setup
from setuptools import find_packages
from everbug import __version__

setup(
    name='everbug',
    version=__version__,
    description='Django debug extension',
    license='MIT',
    platform='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    author='Igor Tolkachnikov',
    author_email='i.tolkachnikov@gmail.com',
    url='https://github.com/everhide/everbug',
    packages=['everbug'],
    include_package_data=True,
    zip_safe=False,
)
