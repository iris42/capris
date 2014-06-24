from setuptools import setup, find_packages
import commandeer

setup(
    name="commandeer",
    version=commandeer.VERSION,
    author="Eugene Eeo",
    author_email="packwolf58@gmail.com",
    pacakges=find_packages(),
    include_package_data=True,
    requires=['envoy']
)
