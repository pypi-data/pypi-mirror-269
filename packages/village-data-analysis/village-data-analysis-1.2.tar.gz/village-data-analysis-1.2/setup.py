from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='village-data-analysis',
    version='1.2',
    packages=find_packages(),
    author='Istvan Gallo',
    author_email='istvan.gallo@lexunit.hu',
    description='Generates report in xlsx and csv format about the inputed geometric shape file within the provided time range.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
