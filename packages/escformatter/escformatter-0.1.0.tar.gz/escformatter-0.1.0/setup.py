from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="escformatter",
    version="0.1.0",
    author="Leonardo S. Amaral",
    author_email="leonardo_amaral98@hotmail.com",
    description="A Python class for executing ANSI escape commands in the console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devleonardoamaral/escformatter.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
