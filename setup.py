from setuptools import setup, find_packages


setup(
    name='FoxLin',
    version='0.0.1',
    author="Misano & MohammadD3veloper",
    description="Foxlin, a simple fast funny json dbms",
    license="GPL3",
    packages=find_packages(exclude=["tests", "handlers", "config"]),
    install_requires=[
        "orjson",
        "pydantic",
        "numpy",
    ],
)
