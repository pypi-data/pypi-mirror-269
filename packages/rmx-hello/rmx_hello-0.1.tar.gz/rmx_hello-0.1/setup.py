# contains the instruction on how to bundle and publish the package
from setuptools import setup, find_packages

setup(
    name='rmx_hello',
    version='0.1',
    packages=find_packages(),
    install_requires= [
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ]
)