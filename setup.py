from setuptools import find_packages, setup

setup(
    name="argus-prime",
    version="0.3",
    packages=find_packages(include=["agents", "agents.*", "capsules", "capsules.*", "integrations", "integrations.*"]),
    install_requires=[],
)
