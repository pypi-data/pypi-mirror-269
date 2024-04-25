# Village data analysis package

## Description

Generates report in xlsx and csv format about the inputed geometric shape file within the provided time range.

## Requirements

To be able to test this code shape file data is required.

## Installation

For installation please use the standard command as follows:
```
pip install village_data_analysis
```

### Sample code:

Please note that the package expects WSG84 formatted geometric shapes. Note that "year n" below supposed to be integers.

```
import village_data_analysis.analyzer as ap

shapefile_paths = [
    ("year 1", "shapeile_1.shp"),
    ("year 2", "shapeile_2.shp"),
    ("year 3", "shapeile_3.shp"),
    ("year n", "shapeile_n.shp"),
]

ap.create_report(shapefile_paths, 2000, 5)
```
