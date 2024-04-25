# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

# Setting up
setuptools.setup(
    name="ggcorrplot", 
    version='0.0.3',
    author="Duvérier DJIFACK ZEBAZE",
    author_email="duverierdjifack@gmail.com",
    description="Visualization of a Correlation Matrix using plotnine",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=["numpy>=1.24.4",
                      "pandas>=2.2.2",
                      "plotnine>=0.10.1",
                      "scipy>=1.10.1"],
    python_requires=">=3.10",
    package_data={"": ["*.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)