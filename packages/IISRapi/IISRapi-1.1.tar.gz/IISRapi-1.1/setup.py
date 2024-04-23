from setuptools import setup, find_packages

setup(
    name='IISRapi',
    version='1.1',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'flair',
        'torch',
        'torchvision',
    ],
)