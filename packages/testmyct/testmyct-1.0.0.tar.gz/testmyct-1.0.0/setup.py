from setuptools import setup, find_packages
import pathlib
 
setup(
    name='testmyct',  # Replace with your actual package name 
    version='1.0.0',
    description="Used for integration with Application monitoring systems",
    long_description = pathlib.Path("README.rst").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # Your project dependencies
    ],
)
