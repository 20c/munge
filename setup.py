
from setuptools import setup, find_packages

version = open('config/VERSION').read().rstrip()

setup(
    name='munge',
    version=version,
    author='Twentieth Century',
    author_email='code@20c.com',
    description='data manipulation client / library',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    scripts=['munge/bin/munge'],
    url = 'https://github.com/20c/munge',
    download_url = 'https://github.com/20c/munge/%s' % version,
    include_package_data=True,
    zip_safe=False
)
