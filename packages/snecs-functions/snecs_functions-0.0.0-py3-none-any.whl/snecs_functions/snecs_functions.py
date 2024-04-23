# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:16:59 2023

@author: cvskf
"""

import urllib
import urllib.request
import json
import os
import sqlite3
import csvw_functions_extra


#_default_data_folder='_data'  # the default
#_default_database_name='snecs_data.sqlite'

urllib.request.urlcleanup()

metadata_document_location=r'https://raw.githubusercontent.com/building-energy/snecs_functions/main/snecs_tables-metadata.json' 

metadata_filename = 'snecs_tables-metadata.json'


#%% data folder

def get_available_csv_file_names(
        ):
    """Returns the CSV file names of all tables in the (remote) CSVW metadata file.
    
    """
    result = \
        csvw_functions_extra.get_available_csv_file_names(
            metadata_document_location = metadata_document_location
            )
    
    return result


def _download_table_group(
        data_folder = '_data',
        csv_file_names = None,  
        verbose = False
        ):
    """
    """
    csvw_functions_extra.download_table_group(
        metadata_document_location = metadata_document_location,
        csv_file_names = csv_file_names,
        data_folder = data_folder,
        overwrite_existing_files = True,
        verbose = verbose
        )
        
    
def _import_table_group_to_sqlite(
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        csv_file_names = None, 
        verbose = False
        ):
    """
    """
    csvw_functions_extra.import_table_group_to_sqlite(
        metadata_filename = metadata_filename,
        csv_file_names = csv_file_names,
        data_folder = data_folder,
        database_name = database_name,
        overwrite_existing_tables = True,
        verbose = verbose
        )
        

def download_and_import_data(
        csv_file_names = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose=False,
        ):
    """
    """
    _download_table_group(
            data_folder = data_folder,
            csv_file_names = csv_file_names,  
            verbose = verbose
            )
    
    _import_table_group_to_sqlite(
            data_folder = data_folder,
            database_name = database_name,
            csv_file_names = csv_file_names, 
            verbose = verbose
            )
    
    
    
def get_snecs_table_names_in_database(
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        ):
    """
    """
    
    result = \
        csvw_functions_extra.get_sql_table_names_in_database(
            data_folder,
            database_name,
            metadata_filename
            )
    
    return result
    
            
    
#%% main functions

def get_government_office_region_elec(
        year = None,
        region_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='elec_GOR_stacked_2005_21'
    
    filter_by = {
        'year':year, 
        'gor':region_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result


def get_government_office_region_gas(
        year = None,
        region_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='gas_GOR_stacked_2005_21'
    
    filter_by = {
        'year':year, 
        'region.code':region_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    

def get_local_authority_elec(
        year = None,
        la_code = None,
        region = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='elec_LA_stacked_2005_21'
    
    filter_by = {
        'year':year, 
        'la_code':la_code, 
        'region':region
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result



def get_local_authority_gas(
        year = None,
        la_code = None,
        region = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='gas_LA_stacked_2005_21'
        
    filter_by = {
        'year':year, 
        'la.code':la_code, 
        'region':region
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result


def get_LSOA_elec_domestic(
        year = None,
        la_code = None,
        msoa_code = None,
        lsoa_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='elec_domestic_LSOA_stacked_2010_21'
    
    filter_by = {
        'YEAR':year, 
        'LACode':la_code, 
        'MSOACode':msoa_code,
        'LSOACode':lsoa_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    

def get_LSOA_gas_domestic(
        year = None,
        la_code = None,
        msoa_code = None,
        lsoa_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='gas_domestic_LSOA_stacked_2010_21'
        
    filter_by = {
        'year':year, 
        'la.name':la_code,  # error in CSV file -> 'name' and 'code' are wrong way round
        'msoa.name':msoa_code,
        'lsoa.name':lsoa_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    

def get_MSOA_elec_domestic(
        year = None,
        la_code = None,
        msoa_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='elec_domestic_MSOA_stacked_2010_21'
    
    filter_by = {
        'year':year, 
        'la.code':la_code, 
        'msoa.code':msoa_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    

def get_MSOA_gas_domestic(
        year = None,
        la_code = None,
        msoa_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='gas_domestic_MSOA_stacked_2010_21'
    
    filter_by = {
        'year':year, 
        'la.code':la_code, 
        'msoa.code':msoa_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    

def get_MSOA_elec_non_domestic(
        year = None,
        la_code = None,
        msoa_code = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='elec_non_domestic_MSOA_stacked_2010_21'
    
    filter_by = {
        'year':year, 
        'la.code':la_code, 
        'msoa.code':msoa_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
     

def get_MSOA_gas_non_domestic(
        year = None,
        la_code = None,
        msoa_code = None,
        fields = None,
        data_folder='_data',
        database_name='snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name='gas_non_domestic_MSOA_stacked_2010_21'
        
    filter_by = {
        'year':year, 
        'la.code':la_code, 
        'msoa.code':msoa_code
        }
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    

def get_postcode_elec_all_meters(
        year,
        postcode = None,
        outcode = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name=f'Postcode_level_all_meters_electricity_{year}'
    
    filter_by = dict(
        Postcode = postcode, 
        Outcode = outcode
        )
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result


def get_postcode_elec_economy_7(
        year,
        postcode = None,
        outcode = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name=f'Postcode_level_economy_7_electricity_{year}'
    
    filter_by = dict(
        Postcode = postcode, 
        Outcode = outcode
        )
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
            

def get_postcode_elec_standard(
        year,
        postcode = None,
        outcode = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    table_name=f'Postcode_level_standard_electricity_{year}'
    
    filter_by = dict(
        Postcode = postcode, 
        Outcode = outcode
        )
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    
    
def get_postcode_gas(
        year,
        postcode = None,
        outcode = None,
        fields = None,
        data_folder = '_data',
        database_name = 'snecs_data.sqlite',
        verbose = False
        ):
    ""
    
    table_name=f'Postcode_level_gas_{year}'
    
    filter_by = dict(
        Postcode = postcode, 
        Outcode = outcode
        )
    filter_by = {k:v for k,v in filter_by.items() if not v is None}
    
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields, 
            verbose = verbose
            )
    
    return result
    
    
    
