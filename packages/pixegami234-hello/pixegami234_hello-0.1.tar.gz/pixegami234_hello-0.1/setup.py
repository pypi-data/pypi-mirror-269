from setuptools import setup, find_packages 

setup(
    name='pixegami234_hello',
    version='0.1',
    packages=find_packages(),
    install_requires=[], 
    entry_points={
        'console_scripts': [
            'saadha-package = pixegami234_hello:hello'
        ]
    }
)