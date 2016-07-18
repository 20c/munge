
from setuptools import setup, find_packages

long_description=open('facsimile/description.txt').readline().strip()
version = open('facsimile/VERSION').readline().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")
test_requirements = open('facsimile/requirements-test.txt').read().split("\n")


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
    test_requires=test_requirements,
    entry_points={
        'console_scripts': [
            'munge=munge.cli:main',
        ]
    },
    zip_safe=False
)
