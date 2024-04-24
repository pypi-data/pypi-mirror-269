from setuptools import setup, find_packages

setup(
    name='akdpy',
    version="0.0.2",
    author="akdogantech",
    description="A small example package",
    packages=find_packages(),
    install_requires=[
        'psutil',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)