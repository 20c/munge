
from setuptools import setup, find_packages

setup(
    name='munge',
    version=open('config/VERSION').read().rstrip(),
    author='Twentieth Century',
    author_email='code@20c.com',
    description='',
    long_description=open('README.md').read(),
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages = find_packages(),
    scripts=['munge/bin/munge'],

    zip_safe=False
)
