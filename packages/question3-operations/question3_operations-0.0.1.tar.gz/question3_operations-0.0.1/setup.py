import setuptools
from setuptools import setup,find_packages


setuptools.setup(
    name="question3_operations",
    version="0.0.7",
    author="PVS.Sukeerthi",
    author_email="sukeerthipolasanapalli@gmail.com",
    description="Python package to do basic math operations",
    url="https://github.com/mahesh-maximus/helloworld-pyp",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={'':"question3_operations"},
    packages=find_packages("question3_operations"),
    python_requires=">=3.6",

)
