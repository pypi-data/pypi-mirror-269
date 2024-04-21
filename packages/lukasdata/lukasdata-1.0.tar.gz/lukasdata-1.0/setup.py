from setuptools import setup, find_packages

setup(
    name='lukasdata',
    packages=find_packages(),
    version="1.0",
    install_requires=[
        "numpy","pandas","json","matplotlib","os"
    ],
)