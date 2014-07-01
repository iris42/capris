from setuptools import setup, find_packages
import capris

setup(
    name="capris",
    version=capris.__version__,
    description="Wrapper for doing beautiful commands",

    long_description=open('README.rst').read(),
    author="Eugene Eeo",
    author_email="packwolf58@gmail.com",
    url='https://github.com/eugene-eeo/capris',

    package_dir={'capris':'capris'},
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    zip_safe=False,

    keywords=['capris','command','wrapper','dsl'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python 2.6',
        'Programming Language :: Python 2.7',
        'Programming Language :: Python 3',
        'Programming Language :: Python 3.3',
        )
)
