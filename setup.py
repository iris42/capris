from setuptools import setup, find_packages
import capris

setup(
    name="capris",
    version=capris.VERSION,
    description="Wrapper for doing beautiful commands",
    long_description=open('README.rst').read(),
    author="Eugene Eeo",
    author_email="packwolf58@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/eugene-eeo/capris'
)
