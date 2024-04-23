from setuptools import setup, find_packages 
from dependencies import install_python_dependencies
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install_python_dependencies()
        install.run(self)


setup(
    name='tests-web',
    version='0.2',
    description='A simple functional test library using Selenium and Chrome driver',
    author='Linda Lopez',
    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
)