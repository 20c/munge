from setuptools import setup, find_packages


def read_file(name):
    with open(name) as fobj:
        return fobj.read().strip()


LONG_DESCRIPTION = read_file("README.md")
version = open("facsimile/VERSION").readline().strip()
requirements = open("facsimile/requirements.txt").read().split("\n")
test_requirements = open("facsimile/requirements-test.txt").read().split("\n")


setup(
    name="munge",
    version=version,
    author="20C",
    author_email="code@20c.com",
    description="data manipulation client / library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="LICENSE.txt",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=requirements,
    test_requires=test_requirements,
    entry_points={"console_scripts": ["munge=munge.cli:main",]},
    zip_safe=False,
)
