from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='llm_offset',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[

    ],
    long_description=description,
    long_description_content_type="text/markdown",

)