from setuptools import setup,find_packages

with open("README.md") as f:
    disc=f.read()


setup(
    name='zking',
    version='0.3',
    packages=find_packages(),
    long_description=disc,
    long_description_content_type="text/markdown",
)