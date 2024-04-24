from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='Project_DataPrepKit',
    version='0.3',
    packages=find_packages(),
    insall_requires=[
        'numpy',
        'pandas'],
    long_description=description,
    long_description_content_type="text/markdown",
    )