# cnspy_csv2dataframe


The class [CSV2DataFrame](./cnspy_csv2dataframe/CSV2DataFrame.py) is intended to load [CSV-files](https://en.wikipedia.org/wiki/Comma-separated_values) into a `pandas.DataFrame`. The CSV files need to match known formats (defined by their header in the first line) according to those defined in the package [spatial_csv_formats]().
  
In case no format is specified, it tries to match the first line of the CSV-File with known headers from [cnspy_spatial_csv_formats](https://github.com/aau-cns/cnspy_spatial_csv_formats) and loads the data in that format. 

There a some specialization of  [CSV2DataFrame](./cnspy_csv2dataframe/CSV2DataFrame.py) that support different operations on the data:
* [PoseCovCSV2DataFrame](./cnspy_csv2dataframe/PosOrientCovCSV2DataFrame.py)
* [PoseWithCov2DataFrame](./cnspy_csv2dataframe/PosOrientWithCov2DataFrame.py)
* [TimestampCSV2DataFrame](./cnspy_csv2dataframe/TimestampCSV2DataFrame.py)
* [TUMCSV2DataFrame](./cnspy_csv2dataframe/TUMCSV2DataFrame.py)

## Installation

Install the current code base from GitHub and pip install a link to that cloned copy
```
git clone https://github.com/aau-cns/cnspy_csv2dataframe.git
cd cnspy_csv2dataframe
pip install -e .
```
or the [official package](https://pypi.org/project/cnspy-csv2dataframe/) via
```commandline
pip install cnspy-csv2dataframe
```

## Dependencies

It is part of the [cnspy eco-system](hhttps://github.com/aau-cns/cnspy_eco_system_test) of the [cns-github](https://github.com/aau-cns) group.  

* [numpy]()
* [pandas]()
* [cnspy_spatial_csv_formats](https://github.com/aau-cns/cnspy_spatial_csv_formats)
* [cnspy_numpy_utils](https://github.com/aau-cns/cnspy_numpy_utils)


## License


Software License Agreement (GNU GPLv3  License), refer to the LICENSE file.

*Sharing is caring!* - [Roland Jung](https://github.com/jungr-ait)
