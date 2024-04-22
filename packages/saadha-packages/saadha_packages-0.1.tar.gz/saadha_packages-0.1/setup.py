from setuptools import setup, find_packages 

setup(
    name='saadha_packages',
    version='0.1',
    packages=find_packages(),
    install_requires=[], 
    entry_points={
        'console_scripts': [
            'saadha-package = saadha_packages:hello'
        ]
    }
)