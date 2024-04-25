from setuptools import setup, find_packages

setup(
    name='village-data-analysis',
    version='1.01',
    packages=find_packages(),
    author='Istvan Gallo',
    author_email='istvan.gallo@lexunit.hu',
    description='Generates report in xlsx and csv format about the inputed geometric shape file within the provided time range.',
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
