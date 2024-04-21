from importlib.metadata import requires

from setuptools import setup

setup(
    name='BiochemPy',
    version='0.4.0',
    url='https://github.com/BohringAtom/BiochemPy',
    author='Steffen Winkler',
    author_email='s.winkler@bioc.uzh.ch',
    requires_python='>=3.11',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
