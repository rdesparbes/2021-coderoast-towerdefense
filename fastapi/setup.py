from setuptools import setup, find_packages


setup(
    name="tower-defense-fastapi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["tower-defense", "fastapi"],
)
