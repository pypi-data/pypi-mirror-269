from setuptools import setup, find_packages

setup(
    name='village-data-analysis',
    version='1.0',
    packages=find_packages(),
    author='Istvan Gallo',
    author_email='istvan.gallo@lexunit.hu',
    description='An analizing package for shapefiles (splits, merges)',
    install_requires=[
        "geopandas",
        "shapely",
        "pyproj",
        "numpy",
        "pandas",
        "tqdm",
        "openpyxl"
    ],
)
