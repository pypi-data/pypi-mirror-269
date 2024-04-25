from setuptools import setup, find_packages

setup(
    name="clump-python",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'numpy-stl',
        'pyvista',
        'scipy',
        'trimesh',
    ],
    author="Utku Canbolat, Vasileios Angelidakis",
    author_email="utku.canbolat@fau.de",
    description="This Python library provides tools for creating and examining clumps using techniques: the Euclidean Distance Transform, Favier, and Ferellec-McDowell. It allows for the efficient generation of clumps and the extraction of their surfaces.",
    license="GPL-3.0-only",
    keywords="Clump, Clump Generation, Euclidean Distance Transform, Favier, Ferellec-McDowell, Surface Extraction",
    url="https://github.com/vsangelidakis/CLUMP",
)
