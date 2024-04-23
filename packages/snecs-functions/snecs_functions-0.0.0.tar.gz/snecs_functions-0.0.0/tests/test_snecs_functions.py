# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:08:36 2023

@author: cvskf
"""

import unittest

from snecs_functions import snecs_functions

import csvw_functions_extra

import datetime
import json
import os


class TestDataFolder(unittest.TestCase):
    ""
    
    def test_get_available_csv_file_names(self):
        ""
        result = snecs_functions.get_available_csv_file_names()
        #print(result)
        self.assertEqual(
            result,
            ['gas_GOR_stacked_2005_21.csv', 
             'elec_GOR_stacked_2005_21.csv', 
             'gas_LA_stacked_2005_21.csv', 
             'elec_LA_stacked_2005_21.csv', 
             'gas_domestic_MSOA_stacked_2010_21.csv', 
             'elec_domestic_MSOA_stacked_2010_21.csv', 
             'gas_domestic_LSOA_stacked_2010_21.csv', 
             'elec_domestic_LSOA_stacked_2010_21.csv', 
             'gas_non_domestic_MSOA_stacked_2010_21.csv', 
             'elec_non_domestic_MSOA_stacked_2010_21.csv', 
             'Postcode_level_gas_2021.csv', 
             'Postcode_level_all_meters_electricity_2021.csv', 
             'Postcode_level_economy_7_electricity_2021.csv', 
             'Postcode_level_standard_electricity_2021_A_to_K.csv', 
             'Postcode_level_standard_electricity_2021_K_to_Z.csv', 
             'Postcode_level_gas_2020.csv', 
             'Postcode_level_all_meters_electricity_2020.csv', 
             'Postcode_level_economy_7_electricity_2020.csv', 
             'Postcode_level_standard_electricity_2020_A_to_K.csv', 
             'Postcode_level_standard_electricity_2020_K_to_Z.csv', 
             'Postcode_level_gas_2019.csv', 
             'Postcode_level_all_meters_electricity_2019.csv', 
             'Postcode_level_economy_7_electricity_2019.csv', 
             'Postcode_level_standard_electricity_2019_A_to_K.csv', 
             'Postcode_level_standard_electricity_2019_K_to_Z.csv', 
             'Postcode_level_gas_2018.csv', 
             'Postcode_level_all_meters_electricity_2018.csv', 
             'Postcode_level_economy_7_electricity_2018.csv', 
             'Postcode_level_standard_electricity_2018_A_to_K.csv', 
             'Postcode_level_standard_electricity_2018_K_to_Z.csv', 
             'Postcode_level_gas_2017.csv', 
             'Postcode_level_all_meters_electricity_2017.csv', 
             'Postcode_level_economy_7_electricity_2017.csv', 
             'Postcode_level_standard_electricity_2017_A_to_K.csv', 
             'Postcode_level_standard_electricity_2017_K_to_Z.csv', 
             'Postcode_level_gas_2016.csv', 
             'Postcode_level_all_meters_electricity_2016.csv', 
             'Postcode_level_economy_7_electricity_2016.csv', 
             'Postcode_level_standard_electricity_2016_A_to_K.csv', 
             'Postcode_level_standard_electricity_2016_K_to_Z.csv', 
             'Postcode_level_gas_2015.csv', 
             'Postcode_level_all_meters_electricity_2015.csv', 
             'Postcode_level_economy_7_electricity_2015.csv', 
             'Postcode_level_standard_electricity_2015_A_to_L.csv', 
             'Postcode_level_standard_electricity_2015_L_to_Z.csv'
             ])


    def _test__download_table_group_LOCAL_METADATA(self):
        ""
        fp_table_group_metadata = \
            os.path.join(os.pardir,'snecs_tables-metadata.json')
        
        csvw_functions_extra.download_table_group(
            metadata_document_location=fp_table_group_metadata,
            data_folder='_data',
            overwrite_existing_files=False,
            verbose=True
            )
        
    def _test__import_table_group_to_sqlite(self):
        ""
        snecs_functions._import_table_group_to_sqlite(
            verbose=True)
    
    
    def _test_download_and_import_data(self):
        ""
        snecs_functions.download_and_import_data(
            verbose=True,
            )


    def test_get_snecs_table_names_in_database(self):
        ""
        result = \
            snecs_functions.get_snecs_table_names_in_database()
        #print(result)
        self.assertEqual(
            result,
            [
                'gas_GOR_stacked_2005_21', 
                'elec_GOR_stacked_2005_21', 
                'gas_LA_stacked_2005_21', 
                'elec_LA_stacked_2005_21', 
                'gas_domestic_MSOA_stacked_2010_21', 
                'elec_domestic_MSOA_stacked_2010_21', 
                'gas_domestic_LSOA_stacked_2010_21', 
                'elec_domestic_LSOA_stacked_2010_21', 
                'gas_non_domestic_MSOA_stacked_2010_21', 
                'elec_non_domestic_MSOA_stacked_2010_21', 
                'Postcode_level_gas_2021', 
                'Postcode_level_all_meters_electricity_2021', 
                'Postcode_level_economy_7_electricity_2021', 
                'Postcode_level_standard_electricity_2021', 
                'Postcode_level_gas_2020', 
                'Postcode_level_all_meters_electricity_2020', 
                'Postcode_level_economy_7_electricity_2020', 
                'Postcode_level_standard_electricity_2020', 
                'Postcode_level_gas_2019', 
                'Postcode_level_all_meters_electricity_2019', 
                'Postcode_level_economy_7_electricity_2019', 
                'Postcode_level_standard_electricity_2019', 
                'Postcode_level_gas_2018', 
                'Postcode_level_all_meters_electricity_2018', 
                'Postcode_level_economy_7_electricity_2018', 
                'Postcode_level_standard_electricity_2018', 
                'Postcode_level_gas_2017', 
                'Postcode_level_all_meters_electricity_2017', 
                'Postcode_level_economy_7_electricity_2017', 
                'Postcode_level_standard_electricity_2017', 
                'Postcode_level_gas_2016', 
                'Postcode_level_all_meters_electricity_2016', 
                'Postcode_level_economy_7_electricity_2016', 
                'Postcode_level_standard_electricity_2016', 
                'Postcode_level_gas_2015', 
                'Postcode_level_all_meters_electricity_2015', 
                'Postcode_level_economy_7_electricity_2015', 
                'Postcode_level_standard_electricity_2015'
                ]
            )
            


class TestMainFunctions(unittest.TestCase):
    ""
    
    def test_get_government_office_region_elec(self):
        ""
        result=snecs_functions.get_government_office_region_elec()
        #print(result[0])
        x={x['gor']:x['region'] for x in result}
        #print(x)
    
    
    def test_get_government_office_region_gas(self):
        ""
        
        result=snecs_functions.get_government_office_region_gas(
            year=2021,
            region_code='E12000004',
            #verbose=True
            )
        #print(result)
        self.assertEqual(
            result,
            [{'year': 2021, 
              'region.code': 'E12000004', 
              'region': 'East Midlands', 
              'domestic.meters': 1881.823, 
              'non.domestic.meters': 19.022, 
              'total.meters': 1900.845, 
              'domestic.sales.gwh': 24686.47417, 
              'non.domestic.sales.gwh': 15226.75651, 
              'total.sales.gwh': 39913.23068, 
              'domestic.mean.kwh': 13118.34081, 
              'non.domestic.mean.kwh': 800481.3642, 
              'mean.kwh': 20997.55882, 
              'domestic.median.kwh': 11719.01385, 
              'non.domestic.median.kwh': 148176.5675, 
              'median.kwh': 11800.46487}]
            )
    
    
    def test_get_local_authority_elec(self):
        ""
        result=snecs_functions.get_local_authority_elec(
            year=2021
            )
        #print(result[0])
        
        
    def test_get_local_authority_gas(self):
        ""
        result=snecs_functions.get_local_authority_gas(
            year=2021
            )
        #print(result[0])
        
        
    def test_LSOA_elec_domestic(self):
        ""
        
        
    def test_get_LSOA_gas_domestic(self):
        ""
        
        result=snecs_functions.get_government_office_region_gas(
            year=2019,
            #region_code='E12000004',
            #verbose=True
            )
        #print(len(result))
        
        
        
        
    def test_get_MSOA_elec_domestic(self):
        ""
        
        
    def test_get_MSOA_gas_domestic(self):
        ""
        
    
    def test_get_MSOA_elec_non_domestic(self):
        ""
        
    def test_get_MSOA_gas_non_domestic(self):
        ""
        
    def test_get_postcode_elec_all_meters(self):
        ""
        
    def test_get_postcode_elec_economy_7(self):
        ""
        
        
    def test_get_postcode_elec_standard(self):
        ""
        
    
    def test_get_postcode_gas(self):
        ""
        
        result=snecs_functions.get_postcode_gas(
            year=2021,
            postcode='LE11 3PE',
            verbose=False
            )
        #print(result)
        self.assertEqual(
            result,
            [{'Outcode': 'LE11', 
              'Postcode': 'LE11 3PE', 
              'Num_meters': 31, 
              'Total_cons_kwh': 502192.22440749354, 
              'Mean_cons_kwh': 16199.749174435276, 
              'Median_cons_kwh': 15071.418638377336}]
            )






    
if __name__=='__main__':
    
    unittest.main()