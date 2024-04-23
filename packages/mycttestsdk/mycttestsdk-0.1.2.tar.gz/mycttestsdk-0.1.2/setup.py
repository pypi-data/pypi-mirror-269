from setuptools import setup, find_packages
import pathlib
 
setup(
    name='mycttestsdk',  # Replace with your actual package name
    # url = 'https://github.com/enomis-dev/test-package', # Replace with your github project link
    version='0.1.2',
    description="Used for integration with Application monitoring systems",
    long_description = pathlib.Path("README.rst").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # Your project dependencies
    ],
)
