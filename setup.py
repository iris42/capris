from setuptools import setup, find_packages
import commandeer

setup(
    name="commandeer",
    version=commandeer.VERSION,
    description="Wrapper for doing beautiful commands",
    long_description=open('README.rst').read(),
    author="Eugene Eeo",
    author_email="packwolf58@gmail.com",
    pacakges=find_packages(),
    include_package_data=True,
    url='https://github.com/eugene-eeo/commandeer'
)
