from setuptools import setup, find_packages

setup(
    author='Group2',
    description='CustomerFrequencyAnalysis',
    name='CustomerFrequency',
    version='0.1.0',
    packages=find_packages(include=['CustomerFrequency', 'CustomerFrequency.*'])
)
