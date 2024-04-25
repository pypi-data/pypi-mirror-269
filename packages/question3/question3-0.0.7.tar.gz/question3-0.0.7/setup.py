import setuptools
from setuptools import setup,find_packages


setuptools.setup(
    name="question3",
    version="0.0.7",
    author="PVS.Sukeerthi",
    author_email="sukeerthipolasanapalli@gmail.com",
    description="Python package to do basic math operations",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={'':"question3"},
    packages=find_packages("question3"),
    python_requires=">=3.6",

)