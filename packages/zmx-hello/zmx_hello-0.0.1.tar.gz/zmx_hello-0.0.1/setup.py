# contains the instruction on how to bundle and publish the package
from setuptools import setup, find_packages

setup(
    name='zmx_hello',
    version='0.0.1',
    packages=find_packages(),
    install_requires= [
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "zmx_hello = zmx_hello:hello"
        ]
    },
    author="rehmet",
    description="A hello world",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"

)