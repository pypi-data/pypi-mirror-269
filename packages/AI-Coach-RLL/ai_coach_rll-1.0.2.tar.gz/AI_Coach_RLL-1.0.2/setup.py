import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()
description="An AI coach under construction"

setuptools.setup(
    name="AI_Coach_RLL",
    version="1.0.2",
    author="Ruofan Yang",
    author_email="13688477617@163.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)