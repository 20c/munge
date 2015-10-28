
from setuptools import setup, find_packages

long_description=open('facsimile/description.txt').read(),
version = open('facsimile/VERSION').read().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")
#test_requirements = open('facsimile/requirements-test.txt').read().split("\n")


setup(
    name='munge',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='data manipulation client / library',
    long_description=long_description,
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages = find_packages(),
    install_requires=requirements,
    scripts=['munge/bin/munge'],

    zip_safe=False
)
