# setup.py example for setuptools
from setuptools import setup, find_packages

setup(
    name="numerical_pde_solver",
    version="0.1.1",
    author="Amit Kumar Jha",
    author_email="jha.8@alumni.iitj.ac.in",
    description="A package for solving PDEs using Euler and Milstein methods",
    packages=find_packages(),
    install_requires=[
        "numpy",  # ensure all dependencies are listed here
    ],
)
