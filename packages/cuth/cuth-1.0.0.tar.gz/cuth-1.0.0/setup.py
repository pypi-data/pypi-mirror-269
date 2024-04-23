from setuptools import setup, find_packages

setup(
    name='cuth',
    version='1.0.0',
    keywords='ceasylog',
    description='A great auth tools',
    author='CandyStar@HuangXudong',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['ceasylog'],
)
