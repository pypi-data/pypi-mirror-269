import setuptools
from setuptools import setup,find_packages

setuptools.setup(
    name="sukeerthiq3",
    version="0.0.7",
    author="PVS.Sukeerthi",
    author_email="sukeerthipolasanapalli@gmail.com",
    description="Python package to do basic math operations",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={'':"src"},
    packages=find_packages("src"),
    python_requires=">=3.6",

)