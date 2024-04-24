from setuptools import setup, find_packages

setup(
    name="mctech_core",
    version="1.0.2",
    packages=find_packages(
        include=["mctech_core**"],
        exclude=["*.test"]
    ),
    install_requires=["log4py", "pyyaml", "pyDes"]
)
