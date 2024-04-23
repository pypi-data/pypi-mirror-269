# snecs_functions
Python package for working with the Sub-National Energy Consumption Statistics dataset

## Overview

The Sub-National Energy Consumption Statistics (SNECS) dataset is published by the UK government here: 
- https://www.gov.uk/government/collections/sub-national-electricity-consumption-data
- https://www.gov.uk/government/collections/sub-national-gas-consumption-data

This Python package contains a series of Python functions which can be used to:
- Download the CSV files which make up the SNECS dataset.
- Import the data into a SQLite database.
- Access the data in the database, for data analysis and visualisation.

A description of the CSV files in the SNECS dataset, along with instructions for downloading and importing in SQLite, has been created using the format of a [CSVW metadata Table Group object](https://www.w3.org/TR/2015/REC-tabular-metadata-20151217/#table-groups) (saved as a JSON file), which is available here: https://raw.githubusercontent.com/building-energy/snecs_functions/main/snecs_tables-metadata.json


## Installation

`pip install snecs_functions`

## Quick Start

```python
import snecs_functions

# downloads all CSV files to folder '_data' and import all the data to SQLite database 'snecs_data.sqlite'
snecs_functions.download_and_import_all_data() 

# view gas consumption in the East Midlands in 2019 and 2020
result = snecs_functions.get_government_office_region_elec(region_code='E12000004' year=[2019,2020])
print(result)
```
```python
[
 {'year': 2019, 'gor': 'E12000004', 'region': 'East Midlands', 'e7_meters': 598.736, 'standard_meters': 1494.085, 'domestic_meters': 2092.821, 'non_domestic_meters': 172.576, 'total_meters': 2265.397, 'e7_sales_gwh': 2607.405573, 'standard_sales_gwh': 4911.897206, 'domestic_sales_gwh': 7519.302779, 'non_domestic_sales_gwh': 12759.67612, 'total_gwh': 20278.9789, 'e7_mean_kwh': 4354.850173, 'e7_median_kwh': 3271.2, 'standard_mean_kwh': 3287.56209, 'standard_median_kwh': 2709.8, 'domestic_mean_kwh': 3592.902966, 'domestic_median_kwh': 2846.6, 'non_domestic_mean_kwh': 73936.56196, 'non_domestic_median_kwh': 8378.45, 'all_mean_kwh': 8951.622561, 'all_median_kwh': 2928.1, 'avg_per_hhld_kwh': 3719.672351}, 
 {'year': 2020, 'gor': 'E12000004', 'region': 'East Midlands', 'e7_meters': 579.852, 'standard_meters': 1532.956, 'domestic_meters': 2112.808, 'non_domestic_meters': 172.466, 'total_meters': 2285.274, 'e7_sales_gwh': 2661.295432, 'standard_sales_gwh': 5337.930295, 'domestic_sales_gwh': 7999.225726, 'non_domestic_sales_gwh': 11468.72202, 'total_gwh': 19467.94775, 'e7_mean_kwh': 4589.611542, 'e7_median_kwh': 3379.3, 'standard_mean_kwh': 3482.115791, 'standard_median_kwh': 2808.8, 'domestic_mean_kwh': 3786.063725, 'domestic_median_kwh': 2941.2, 'non_domestic_mean_kwh': 66498.45199, 'non_domestic_median_kwh': 6556.95, 'all_mean_kwh': 8518.868087, 'all_median_kwh': 3002.1, 'avg_per_hhld_kwh': 3923.50087}
]
```

## API

### get_available_csv_file_names

Description: Returns the CSV file names of all tables in the [CSVW metadata file](https://raw.githubusercontent.com/building-energy/snecs_functions/main/snecs_tables-metadata.json).

```python
snecs_functions.get_available_csv_file_names()
```

Returns: A list of the `https://purl.org/berg/csvw_functions_extra/vocab/csv_file_name` value in each table.


### download_and_import_data

Description: Downloads all the SNECS data and imports all data into a SQLite database.

```python
snecs_functions.download_and_import_data(
        csv_file_names = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False,
        )
```

The data to be downloaded is described in the CSVW metadata file here: https://raw.githubusercontent.com/building-energy/snecs_functions/main/snecs_tables-metadata.json

Running this function will:
- create the `data_folder` if it does not already exist.
- download the CSV files to the data folder.
- download the CSVW metadata file to the data folder. This is named 'snecs_tables-metadata.json'.
- create a SQLite database named `database_name` in the data folder if it does not already exist.
- import the CSV data into the SQLite database.

Arguments:
- **csv_file_names** *(str, list or None)*: The CSV file name(s) to download and import (see [`get_available_csv_file_names`](#get_available_csv_file_names)). `None` will download the entire dataset.
- **data_folder** *(str)*: The filepath of a local folder where the downloaded CSV data is saved to and the SQLite database is stored.
- **database_name** *(str)*: The name of the SQLite database, relative to the data_folder.
- **verbose (bool)**: If True, then this function prints intermediate variables and other useful information.

Returns: None


### get_snecs_table_names_in_database

Description: Returns the table names of all SNECS tables in the SQLite database.

```python
snecs_functions.get_snecs_table_names_in_database(
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        )
```

Returns: A list of table names.


### get_government_office_region_elec

Description: Returns the electricity statistics for government office regions.

```python
snecs_functions.get_government_office_region_elec(
        year=None,
        region_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **region_code** *(str or list)*: ONS region code(s) to filter by (e.g. 'E12000004')

Returns: A list of results dictionaries, based on the rows in the data table.


### get_government_office_region_gas

Description: Returns the gas statistics for government office regions.

```python
snecs_functions.get_government_office_region_gas(
        year=None,
        region_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **region_code** *(str or list)*: ONS region code(s) to filter by (e.g. 'E12000004')

Returns: A list of results dictionaries, based on the rows in the data table.


### get_local_authority_elec

Description: Returns the electricity statistics for local authority regions.

```python
snecs_functions.get_local_authority_elec(
        year=None,
        la_code=None,
        region=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **region** *(str or list)*: Region name(s) to filter by (i.e. 'North East')

Returns: A list of results dictionaries, based on the rows in the data table.


### get_local_authority_gas

Description: Returns the gas statistics for local authority regions.

```python
snecs_functions.get_local_authority_gas(
        year=None,
        la_code=None,
        region=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **region** *(str or list)*: Region name(s) to filter by (i.e. 'North East')

Returns: A list of results dictionaries, based on the rows in the data table.


### get_LSOA_elec_domestic

Description: Returns the domestic electricity statistics for Lower Super Output Areas.

```python
snecs_functions.get_LSOA_elec_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        lsoa_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **msoa_code** *(str or list)*: ONS MSOA code(s) to filter on
- **lsoa_code** *(str or list)*: ONS LSOA code(s) to filter on

Returns: A list of results dictionaries, based on the rows in the data table.


### get_LSOA_gas_domestic

Description: Returns the domestic gas statistics for Lower Super Output Areas.

```python
snecs_functions.get_LSOA_gas_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        lsoa_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **msoa_code** *(str or list)*: ONS MSOA code(s) to filter on
- **lsoa_code** *(str or list)*: ONS LSOA code(s) to filter on

Returns: A list of results dictionaries, based on the rows in the data table.


### get_MSOA_elec_domestic

Description: Returns the domestic electricity statistics for Middle Super Output Areas.

```python
snecs_functions.get_MSOA_elec_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **msoa_code** *(str or list)*: ONS MSOA code(s) to filter on

Returns: A list of results dictionaries, based on the rows in the data table.


### get_MSOA_gas_domestic

Description: Returns the doemstic gas statistics for Middle Super Output Areas.

```python
snecs_functions.get_MSOA_gas_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **msoa_code** *(str or list)*: ONS MSOA code(s) to filter on

Returns: A list of results dictionaries, based on the rows in the data table.


### get_MSOA_elec_non_domestic

Description: Returns the non-domestic electricity statistics for Middle Super Output Areas.

```python
snecs_functions.get_MSOA_elec_non_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **msoa_code** *(str or list)*: ONS MSOA code(s) to filter on

Returns: A list of results dictionaries, based on the rows in the data table.


### get_MSOA_gas_non_domestic

Description: Returns the non-domestic gas statistics for Middle Super Output Areas.

```python
snecs_functions.get_MSOA_gas_non_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int or list)*: Year(s) to filter by (2015 - 2021)
- **la_code** *(str or list)*: ONS local authority code(s) to filter by (e.g. 'E06000001')
- **msoa_code** *(str or list)*: ONS MSOA code(s) to filter on

Returns: A list of results dictionaries, based on the rows in the data table.


### get_postcode_elec_all_meters

Description: Returns the electricity statistics for all meters for postcodes.

```python
snecs_functions.get_postcode_elec_all_meters(
        year,
        postcode=None,
        outcode=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```

Arguments:
- **year** *(int)*: The year to filter by (2015 - 2021)
- **postcode** *(str or list)*: The postcode(s) to filter by
- **outcode** *(str or list)*: The outcode(s) to filter by

Returns: A list of results dictionaries, based on the rows in the data table.


### get_postcode_elec_economy_7

Description: Returns the electricity statistics for economy 7 meters for postcodes.

```python
snecs_functions.get_postcode_elec_economy_7(
        year,
        postcode=None,
        outcode=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```
Arguments:
- **year** *(int)*: The year to filter by (2015 - 2021)
- **postcode** *(str or list)*: The postcode(s) to filter by
- **outcode** *(str or list)*: The outcode(s) to filter by

Returns: A list of results dictionaries, based on the rows in the data table.


### get_postcode_elec_standard

Description: Returns the electricity statistics for standard meters for postcodes.

```python
snecs_functions.get_postcode_elec_standard(
        year,
        postcode=None,
        outcode=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```
Arguments:
- **year** *(int)*: The year to filter by (2015 - 2021)
- **postcode** *(str or list)*: The postcode(s) to filter by
- **outcode** *(str or list)*: The outcode(s) to filter by

Returns: A list of results dictionaries, based on the rows in the data table.


### get_postcode_gas

Description: Returns the gas statistics for postcodes.

```python
snecs_functions.get_postcode_gas(
        year,
        postcode=None,
        outcode=None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose=False
        )
```
Arguments:
- **year** *(int)*: The year to filter by (2015 - 2021)
- **postcode** *(str or list)*: The postcode(s) to filter by
- **outcode** *(str or list)*: The outcode(s) to filter by

Returns: A list of results dictionaries, based on the rows in the data table.

