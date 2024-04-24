from setuptools import setup, find_packages

setup(
    name='lukasdata',
    packages=find_packages(),
    version="1.1",
    install_requires=["numpy","pandas","matplotlib"
    ]
)