from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="astabc",
    version="0.1.11",
    author="Guillaume Descoteaux-Isabelle",
    description="A Python module for automatic brightness and contrast optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgwill/gia-abc",
    packages=["astabc"],
    entry_points={
        "console_scripts": ["astabc=astabc.astabc:main","abc=astabc.astabc:main"],
    },
    install_requires=["opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
