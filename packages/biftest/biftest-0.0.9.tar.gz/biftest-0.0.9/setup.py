from setuptools import setup, find_packages

setup(
name='biftest',
version='0.0.9',
packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'matplotlib>=3.1',
        'requests',
        'seaborn>=0.10'
    ]
)