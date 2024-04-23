# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 14:47:35 2023

@author: cvskf
"""

# This module contains extra functions based on the CSVW format.
# These are not part of the CSVW standards, rather additional functionality.

import csvw_functions
import os
import json
import urllib.request
import urllib.parse
import sqlite3
import subprocess
import zipfile
# import pandas as pd


#%% remote csvw metadata functions

def get_normalized_metadata_table_group_dict(
        metadata_document_location
        ):
    """
    """
    metadata_table_group_dict = \
        csvw_functions.validate_table_group_metadata(
            metadata_document_location
            )
        
    return metadata_table_group_dict
    

def get_available_csv_file_names(
        metadata_document_location
        ):
    """
    """
    metadata_table_group_dict = \
        get_normalized_metadata_table_group_dict(
                metadata_document_location
                )
    
    result = []
    
    for metadata_table_dict in metadata_table_group_dict['tables']:
    
        x = metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/csv_file_name')
        
        if not x is None:
            
            result.append(x['@value'])
        
    return result



#%% download csv files

def download_table_group(
        metadata_document_location,
        data_folder,
        csv_file_names=None,  # if none then all are downloaded
        overwrite_existing_files=False,
        verbose=False
        ):
    """Reads a CSVW metadata file and downloads the CSV files from remote locations.
    
    This makes use of the https://purl.org/berg/csvw_functions_extra vocabulary.
        
    :param metadata_document_location: The filepath of the csvw metadata 
        file containing a table group object.
    :type metadata_document_location: str
    
    :param data_folder: The filepath of a local folder where the 
        downloaded CSV data is to be saved to.
    :type data_folder: str
    
    :param csv_file_names: The csv_file_name values of the tables 
        to be downloaded. If None then all tables are downloaded.
    :type csv_file_names: str or list
    
    :param overwrite_existing_files: If True, then any existing CSV files
        in data_folder will be overwritten. 
        If False, then no download occurs if there is an existing CSV file
        in data_folder.
    :type overwrite_existing_files: bool
    
    :param verbose: If True, then this function prints intermediate variables
        and other useful information.
    :type verbose: bool
    
    :returns: The local filepath of the updated csvw metadata file 
        containing the new URLs for the newly downloaded tables.
    :rtype: str
    
    """
    if verbose:
        print('--- FUNCTION: csvw_functions_extra.download_table_group ---')
    
    # convert single csv_file_name to list. None becomes an empty list.
    csv_file_name_list=convert_to_iterator(csv_file_names)
    
    # create data_folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        
    # get normalised metadata_table_group_dict
    metadata_table_group_dict = \
        csvw_functions.validate_table_group_metadata(
            metadata_document_location
            )
    #if verbose:
        #print(metadata_table_group_dict)
    
    for i, metadata_table_dict in enumerate(metadata_table_group_dict['tables']):
        
        download_info=_get_download_info(
            metadata_table_dict,
            data_folder,
            verbose=False,
            )
        
        # download table - if required
        if len(csv_file_name_list)==0 \
            or download_info['csv_file_name'] in csv_file_name_list:
                
            if verbose:
                print('---')
                for k,v in download_info.items(): print(k,v)
        
            _download_table_and_metadata(
                overwrite_existing_files=overwrite_existing_files,
                verbose=verbose,
                **download_info
                )
            
            if verbose:
                print('---')
    
        # update metadata_table_dict
        metadata_table_dict['url']=download_info['csv_file_name']
        
           
        
    # save updated metadata_table_group_dict
    fp_metadata=os.path.join(data_folder,os.path.basename(metadata_document_location))
    with open(fp_metadata, 'w') as f:
        json.dump(metadata_table_group_dict,f,indent=4)
        
    return fp_metadata
    

def _get_download_info(
        metadata_table_dict,
        data_folder,
        verbose=False
        ):
    ""
    # get info for downloading
    csv_file_name=metadata_table_dict['https://purl.org/berg/csvw_functions_extra/vocab/csv_file_name']['@value']
    if verbose:
        print('csv_file_name:',csv_file_name)
    csv_download_url=metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/csv_download_url',{'@value':None})['@value']
    if verbose:
        print('csv_download_url:', csv_download_url)
    zip_download_url=metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/zip_download_url',{'@value':None})['@value']
    if verbose:
        print('zip_download_url',zip_download_url)
    zip_file_name=metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/zip_file_name',{'@value':None})['@value']
    if verbose:
        print('zip_file_name',zip_file_name)
    csv_zip_extract_path=metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/csv_zip_extract_path',{'@value':None})['@value']
    if verbose:
        print('csv_zip_extract_path',csv_zip_extract_path)
    metadata_url=metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/metadata_download_url',{'@value':None})['@value']
    if verbose:
        print('metadata_url:',metadata_url)
    metadata_file_suffix=metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/metadata_file_suffix',{'@value':'-metadata.txt'})['@value']
    if verbose:
        print('metadata_file_suffix:',metadata_file_suffix)
    
    fp_csv=os.path.join(data_folder,csv_file_name)
    if verbose:
        print('fp_csv',fp_csv)
    if zip_file_name is None:
        fp_zip = None
    else:
        fp_zip=os.path.join(data_folder, zip_file_name)
    if verbose:
        print('fp_zip:', fp_zip)
    
    result = dict(
        csv_file_name=csv_file_name, 
        csv_download_url=csv_download_url, 
        zip_download_url=zip_download_url, 
        zip_file_name=zip_file_name,
        csv_zip_extract_path=csv_zip_extract_path,
        metadata_url=metadata_url,
        metadata_file_suffix=metadata_file_suffix,
        fp_csv=fp_csv,
        fp_zip=fp_zip
        )
    
    return result


def _download_table_and_metadata(
        csv_download_url=None,
        fp_csv=None,
        zip_download_url=None,
        fp_zip=None,
        csv_zip_extract_path=None,
        metadata_url=None,
        metadata_file_suffix=None,
        overwrite_existing_files=False,
        verbose=False,
        **kwargs  # to pick up unused keywords in **download_info
        ):
    """
    """
    
    if not csv_download_url is None:
        
        # download csv
        if overwrite_existing_files or not os.path.exists(fp_csv):
            
            urllib.request.urlretrieve(
                url=csv_download_url, 
                filename=fp_csv
                )
            
    else:  # zip file
        
        # download zip
        if not zip_download_url is None:
        
            if overwrite_existing_files or not os.path.exists(fp_zip):
                
                if verbose:
                    print('downloading zip file...')
                urllib.request.urlretrieve(
                    url=zip_download_url, 
                    filename=fp_zip
                    )
        
        # extract csv
        if overwrite_existing_files or not os.path.exists(fp_csv):
            
            if verbose:
                print('extracting csv file...')
            with zipfile.ZipFile(fp_zip) as z:
    
                with open(fp_csv, 'wb') as f:
                    
                    f.write(z.read(csv_zip_extract_path))
              
            
    # download metadata
    if not metadata_url is None:
        
        if not csv_download_url is None:
        
            fp_metadata=f"{fp_csv}-{metadata_file_suffix}"
            
        else:
            
            fp_metadata=f"{fp_zip}-{metadata_file_suffix}"
        
        if overwrite_existing_files or not os.path.exists(fp_metadata):
            
            urllib.request.urlretrieve(
                url=metadata_url, 
                filename=fp_metadata
                )
            
        

#%% downloaded csvw metadata file


def get_metadata_table_group_dict(
        data_folder,
        metadata_filename
        ):
    ""
    fp=os.path.join(
        data_folder,
        metadata_filename
        )
    with open(fp) as f:
        metadata_table_group_dict=json.load(f)
        
    return metadata_table_group_dict


def get_metadata_table_dict(
        sql_table_name,
        metadata_table_group_dict = None,
        data_folder = None,
        metadata_filename = None
        ):
    ""
    if metadata_table_group_dict is None:
        
        metadata_table_group_dict = \
            get_metadata_table_group_dict(
                data_folder = data_folder,
                metadata_filename = metadata_filename
                )
    
    for metadata_table_dict in metadata_table_group_dict['tables']:
        
        if metadata_table_dict['https://purl.org/berg/csvw_functions_extra/vocab/sql_table_name']['@value']==sql_table_name:
            
            break
        
    else:
        
        raise Exception
    
    return metadata_table_dict
    

def get_metadata_column_dict(
        column_name,
        sql_table_name,
        metadata_table_group_dict = None,
        data_folder = None,
        metadata_filename = None
        ):
    ""
    if metadata_table_group_dict is None:
        
        metadata_table_group_dict = \
            get_metadata_table_group_dict(
                data_folder = data_folder,
                metadata_filename = metadata_filename
                )
            
    metadata_table_dict = \
        get_metadata_table_dict(
               sql_table_name,
               metadata_table_group_dict
               )
    
    for metadata_column_dict in metadata_table_dict['tableSchema']['columns']:
        
        if metadata_column_dict['name'] == column_name:
            
            break
        
    else:
        
        raise Exception
    
    return metadata_column_dict
    

def get_metadata_sql_table_names(
        metadata_table_group_dict = None,
        data_folder = None,
        metadata_filename = None
        ):
    """
    """
    if metadata_table_group_dict is None:
        
        metadata_table_group_dict = \
            get_metadata_table_group_dict(
                data_folder,
                metadata_filename
                )

    result=[]
    
    for metadata_table_dict in metadata_table_group_dict['tables']:
        
        x = metadata_table_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/sql_table_name')
        
        if not x is None:
            
            result.append(x['@value'])
            
    return result



def get_metadata_columns_codes(
        sql_table_name,
        column_names = None,
        metadata_table_group_dict = None,
        data_folder = None,
        metadata_filename = None
        ):
    """
    """
    metadata_table_dict = \
        get_metadata_table_dict(
            sql_table_name,
            metadata_table_group_dict = metadata_table_group_dict,
            data_folder = data_folder,
            metadata_filename = metadata_filename
            )
        
    if column_names is None:
        column_names = \
            [metadata_column_dict['name'] 
             for metadata_column_dict 
             in metadata_table_dict['tableSchema']['columns']
             ]
            
    column_names = convert_to_iterator(column_names)
    
    result = {}
    
    for metadata_column_dict in metadata_table_dict['tableSchema']['columns']:
        
        if metadata_column_dict['name'] in column_names:
            
            datatype_base = metadata_column_dict['datatype']['base']
                
            codes = metadata_column_dict.get(
                'https://purl.org/berg/csvw_functions_extra/vocab/codes',
                {}
                )
            
            if datatype_base == 'integer':
                x=lambda y:int(y) if y!='' else y
            elif datatype_base in ['decimal','number']:
                x=lambda y:float(y) if y!='' else y
            elif datatype_base == 'string':
                x=lambda y:y
            else:
                raise Exception
            
            codes = {x(k):v['@value'] for k,v in codes.items()}
            
            result[metadata_column_dict['name']] = codes

    return result


#%% import data to sqlite

def import_table_group_to_sqlite(
        metadata_filename,
        data_folder,
        database_name,
        csv_file_names=None,  # if none then all are imported
        overwrite_existing_tables=False,
        verbose=False
        ):
    """
    Reads a CSVW metadata file and imports the CSV data into a SQLITE database.
    
    This makes use of the https://purl.org/berg/csvw_functions_extra vocabulary.
        
    :param metadata_document_location: The filepath of the csvw metadata 
        file containing a table group object.
    :type metadata_document_location: str
    
    :param data_folder: The filepath of a local folder where the 
        downloaded CSV data is located and the SQLITE database is stored.
    :type data_folder: str
    
    :param database_name: The name of the SQLITE database, relative to the
        data_folder.
    :type database_name: str
    
    :param csv_file_names: The csv_file_name values of the tables 
        to be imported. If None then all tables are imported.
    :type csv_file_names: str or list
    
    :param overwrite_existing_tables: If True, then before importing the CSV data
        any associated existing table in the database is removed and recreated.
    :type overwrite_existing_tables: bool
    
    :param verbose: If True, then this function prints intermediate variables
        and other useful information.
    :type verbose: bool
    
    :returns: None
    
    """
    if verbose:
        print('--- FUNCTION: csvw_functions_extra.import_table_group_to_sqlite ---')
    
    # convert single csv_file_name to list. None becomes an empty list.
    csv_file_name_list=convert_to_iterator(csv_file_names)
        
    # create data_folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        
    # set database fp
    fp_database=os.path.join(data_folder,database_name)
    
    # get normalised metadata_table_group_dict
    metadata_table_group_dict = \
        get_metadata_table_group_dict(
                data_folder,
                metadata_filename
                )
    #print(metadata_table_group_dict)
    
    # remove existing tables if requested
    for metadata_table_dict in metadata_table_group_dict['tables']:
    
        # get import info
        csv_file_name, table_name, fp_csv, remove_existing_table = \
            _get_import_info(
                metadata_table_dict,
                data_folder,
                verbose=False,
                ) 
        
        # if requested by csv_file_name argument
        if len(csv_file_name_list)==0 \
            or csv_file_name in csv_file_name_list:
                
            if verbose:
                print('---')
                print('csv_file_name',csv_file_name)
                print('table_name',table_name)
                print('fp_csv',fp_csv)
                print('remove_existing_table',remove_existing_table)
                
            if _check_if_table_exists_in_database(
                fp_database, 
                table_name
                ):
                
                if remove_existing_table or overwrite_existing_tables:
    
                    _drop_table(
                        fp_database,
                        table_name
                        )
        
    # create and import tables
    for metadata_table_dict in metadata_table_group_dict['tables']:
        
        # get import info
        csv_file_name, table_name, fp_csv, remove_existing_table = _get_import_info(
                metadata_table_dict,
                data_folder,
                verbose=False,
                ) 
            
        if len(csv_file_name_list)==0 \
            or csv_file_name in csv_file_name_list:
            
            # create empty table if needed
            if not _check_if_table_exists_in_database(
                    fp_database, 
                    table_name
                    ):
                
                _create_table_from_csvw(
                    metadata_table_dict, 
                    fp_database, 
                    table_name)
                
            # import table data to database
            _import_csv_file(
                    fp_csv,
                    fp_database,
                    table_name,
                    verbose=verbose
                    )
        
            if verbose:
                print('---')
            

def _check_if_table_exists_in_database(
        fp_database,
        table_name
        ):
    ""
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query=f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        return True if c.execute(query).fetchall()[0][0] else False


def _create_table_from_csvw(
        metadata_table_dict,
        fp_database,
        table_name,
        verbose=False
        ):
    ""
    # create query
    datatype_map={
    'integer':'INTEGER',
    'decimal':'REAL'
    }
    query=f'CREATE TABLE "{table_name}" ('
    for column_dict in metadata_table_dict['tableSchema']['columns']:
        #print(column_dict)
        name=column_dict['name']
        datatype=datatype_map.get(column_dict['datatype']['base'],'TEXT')
        query+=f'"{name}" {datatype}'
        query+=", "
    query=query[:-2]
    
    if 'primaryKey' in metadata_table_dict['tableSchema']:
        
        pk=metadata_table_dict['tableSchema']['primaryKey']
        if isinstance(pk,str):
            pk=[pk]
        query+=', PRIMARY KEY ('
        for x in pk:
            query+=f'"{x}"'
            query+=", "
        query=query[:-2]
        query+=') '
    
    query+=');'
    
    if verbose:
        print('---QUERY TO CREATE TABLE---')
        print(query)
    
    # create empty table in database
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        
    # create indexes
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        for column_dict in metadata_table_dict['tableSchema']['columns']:
            column_name=column_dict['name']
            setindex=column_dict.get('https://purl.org/berg/csvw_functions_extra/vocab/sqlsetindex',False)
            if setindex:
                index_name=f'{table_name}_{column_name}'
                query=f'CREATE INDEX "{index_name}" ON "{table_name}"("{column_name}")'
                if verbose:
                    print(query)
                c.execute(query)
                conn.commit()
                

def _drop_table(
        fp_database,
        table_name,
        verbose=False
        ):
    ""
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query=f'DROP TABLE IF EXISTS "{table_name}";'
        if verbose:
            print(query)
        c.execute(query)
        conn.commit()


def _get_import_info(
        metadata_table_dict,
        data_folder,
        verbose=False,
        ):
    ""
    # get info for importing
    csv_file_name=metadata_table_dict['https://purl.org/berg/csvw_functions_extra/vocab/csv_file_name']['@value']
    if verbose:
        print('csv_file_name:',csv_file_name)
    table_name=metadata_table_dict['https://purl.org/berg/csvw_functions_extra/vocab/sql_table_name']['@value']
    if verbose:
        print('table_name:',table_name)
    url=metadata_table_dict['url']
    if verbose:
        print('url',url)
    fp_csv=os.path.join(data_folder,url)
    if verbose:
        print('fp_csv:', fp_csv)
    remove_existing_table=metadata_table_dict.get(
        "https://purl.org/berg/csvw_functions_extra/vocab/sql_remove_existing_table",
        False
        )
    
    return csv_file_name,table_name, fp_csv, remove_existing_table
    
    
def _get_row_count_in_database_table(
        fp_database,
        table_name,
        column_name='*'
        ):
    """Gets number of rows in table
    
    """
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query=f'SELECT COUNT({column_name}) FROM "{table_name}"'
        return c.execute(query).fetchone()[0]
    
        
def _import_csv_file(
        fp_csv,
        fp_database,
        table_name,
        verbose=False
        ):
    """
    """                
    fp_database2=fp_database.replace('\\','\\\\')
    fp_csv2=fp_csv.replace('\\','\\\\')
    command=f'sqlite3 {fp_database2} -cmd ".mode csv" ".import --skip 1 {fp_csv2} {table_name}"'
    if verbose:
        print('COMMAND LINE', command)
    subprocess.run(command)
    if verbose:
        print('Number of rows after import: ', _get_row_count_in_database_table(fp_database,table_name))



      
        
#%% database functions

def add_index(
        fields,
        table_name,
        data_folder,
        database_name,
        unique=False,
        verbose=False
        ):
    ""
    fields=convert_to_iterator(fields)
    fields_string='__'.join(fields)
    
    if unique:
        unique_string='UNIQUE'
    else:
        unique_string=''
    
    index_name=f'index__{table_name}__{fields_string}'
    if unique:
        index_name=f'{index_name}__UNIQUE'
    
    if verbose:
        print('index_name',index_name)
        
    column_list='","'.join(fields)
    column_list=f'"{column_list}"'
        
    fp_database=os.path.join(data_folder,database_name)
    
    query=f"""
        CREATE {unique_string} INDEX "{index_name}" 
        ON "{table_name}"({column_list});
    """
    if verbose:
        print('fp_database',fp_database)
        print(query)
        
    try:
        
        with sqlite3.connect(fp_database) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            
    except sqlite3.OperationalError:
        
        if verbose:
            print('Index not created - already exists in table')

        
def get_all_table_names_in_database(
        data_folder,
        database_name        
        ):
    """
    """
    fp_database=os.path.join(data_folder,database_name)
    
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        result = c.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()

    result = [x[0] for x in result]
    
    return result


def get_field_names(
        table_name,
        data_folder,
        database_name,
        verbose=False
        ):
    ""
    fp_database=os.path.join(data_folder,database_name)
    
    if verbose:
        print('fp_database:',fp_database)
        
        
    query=f'PRAGMA table_info({table_name});'
    if verbose:
        print(query)
        
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        
        return [x[1] for x in c.execute(query).fetchall()]
    
    
    
def get_row_count(
        table_name,
        data_folder,
        database_name,
        filter_by=None,
        group_by=None,
        verbose=False
        ):
    ""
    fp_database=os.path.join(data_folder,database_name)
    if verbose:
        print('fp_database:',fp_database)
    
    where_string=\
        get_where_string(
            filter_by
            )
    if verbose:
        print('where_string', where_string)
        
    group_by_fields, group_by_string = \
        get_group_by_string(
            group_by
            )
    if verbose:
        print('group_by_fields',group_by_fields)
        print('group_by_string',group_by_string)
        
    query=f"""
        SELECT 
            {group_by_fields} COUNT(*) AS COUNT
        FROM 
            {table_name} 
        {where_string}
        {group_by_string}
        """
        
    if verbose:
        print(query)
            
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result


def get_rows(
        table_name,
        data_folder,
        database_name,
        filter_by = None,  # a dict
        fields = None,  # or a list of field names
        limit = None,
        # pandas = False,
        replace_codes = False,
        metadata_filename = None,  # needed if using replace codes
        verbose = False
        ):
    ""
    fp_database = os.path.join(data_folder,database_name)
    
    field_string = \
        get_field_string(
            fields
            )
    
    where_string = \
        get_where_string(
            filter_by
            )
        
    if limit is None:
        limit_string = ''
    else:
        limit_string = f' LIMIT {limit} '
        
    query=f"""
        SELECT 
            {field_string}
        FROM 
            {table_name} 
            {where_string}
        {limit_string}
        """
        
    if verbose:
        print(query)
        
        
    # get data
    with sqlite3.connect(fp_database) as conn:
        
        # if pandas:
            
        #     result = pd.read_sql(query,conn)
                
        # else:
            
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    
    # replace codes
    if replace_codes:
        
        codes = \
            get_metadata_columns_codes(
                    sql_table_name = table_name,
                    column_names = None,
                    data_folder = data_folder,
                    metadata_filename = metadata_filename
                    )
            
        if isinstance(result,list):  # it's a list of dictionaries
            
            for row_dict in result:
                
                for field, value in row_dict.items():
                    
                    lookup_dict = codes.get(field)
                    
                    row_dict[field] = lookup_dict.get(value,value)
            
        else:  # it's a Pandas dataframe
            
            for col in result.columns:
                
                result[col] = result[col].replace(codes.get(col,{}))
                
        
    return result



def get_sql_table_names_in_database(
        data_folder,
        database_name,
        metadata_filename
        ):
    """
    """
    sql_table_names = \
        get_metadata_sql_table_names(
                metadata_table_group_dict = None,
                data_folder = data_folder,
                metadata_filename = metadata_filename
                )
    #print('sql_table_names',sql_table_names)
            
    all_table_names = \
        get_all_table_names_in_database(
                data_folder = data_folder,
                database_name = database_name       
                )
    #print('all_table_names',all_table_names)
    
    result=[x for x in all_table_names if x in sql_table_names]
    
    return result
    


def run_sql(
        sql_query,
        data_folder,
        database_name,
        verbose=False
        ):
    ""
    fp_database=os.path.join(data_folder,database_name)
    
    if verbose:
        print('fp_database',fp_database)
        print(sql_query)
        
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(sql_query).fetchall()]
        
    return result


#%% utility functions

def convert_to_iterator(
        x
        ):
    ""
    if x is None:
        return []
    elif isinstance(x,str):
        return [x]
    else:
        try:   
            _ = iter(x)
            return x
        except TypeError:
            return [x]
        
        
def get_field_string(
        fields = None
        ):
    ""
    if fields is None or fields=='':
        fields_string='*'
    else:
        fields=convert_to_iterator(fields)
        fields_string='","'.join(fields)
        fields_string=f' "{fields_string}" '
    
    return fields_string


def get_group_by_string(
        group_by = None
        ):
    ""
    if group_by is None:
        groups=[]
    else:
        groups=convert_to_iterator(group_by)
        
    if len(groups)==0:
        group_by_fields=''
        group_by_string=''
    else:
        x='","'.join(groups)
        group_by_fields=f' "{x}", '
        group_by_string=f'GROUP BY "{x}" '
        
    return group_by_fields, group_by_string


def get_where_string(
        filter_by = None # a dict
        ):
    ""
    if filter_by is None:
        
        filter_by=dict()
    
    where = []
    
    for field_name,filter_value in filter_by.items():
        
        if isinstance(filter_value,dict):
            
            if len(filter_value) > 1:
                raise Exception  # only a single filter keyword to be passed
                
            filter_keyword = list(filter_value.keys())[0]
            filter_values = list(filter_value.values())[0]
            
            if filter_keyword == 'BETWEEN':
                
                filter_values = convert_to_iterator(filter_values)
                
                if not len(filter_values) == 2:
                    
                    raise Exception
                    
                else:
                    
                    filter_string_list = []
                    for x in filter_values:
                        if isinstance(x,str):
                            filter_string_list.append(f'"{x}"')
                        elif isinstance(x,bool):
                            filter_string_list.append(f'{x}')
                        else:
                            filter_string_list.append(f'{x}')
                    filter_string=' AND '.join(filter_string_list)
                    filter_string=f'({filter_string})'
                    filter_operator='BETWEEN'
                        
            else:
                
                raise NotImplementedError
            
        else:
        
            filter_values=convert_to_iterator(filter_value)
            
            if len(filter_values) == 0:
                filter_string = 'Null'
                filter_operator = '='
                
            elif len(filter_values) == 1:
                x = filter_values[0]
                if isinstance(x,str):
                    filter_string=f'"{x}"'
                else:
                    filter_string=f'{x}'
                filter_operator='='
            else:
                filter_string_list = []
                for x in filter_values:
                    if isinstance(x,str):
                        filter_string_list.append(f'"{x}"')
                    elif isinstance(x,bool):
                        filter_string_list.append(f'{x}')
                    else:
                        filter_string_list.append(f'{x}')
                filter_string=','.join(filter_string_list)
                filter_string=f'({filter_string})'
                filter_operator='IN'
            
        where.append(f'("{field_name}" {filter_operator} {filter_string})')
    
    if len(where)==0:
        where_string=''
    else:
        x=' AND '.join(where)
        where_string=f' WHERE {x}'

    return where_string
        
        
              
        
        
        

# def import_table_to_sqlite(
#         metadata_document_location,
#         data_folder='_data',
#         database_name='data.sqlite',
#         verbose=True,
#         _reload_database_table=False
#         ):
#     """
#     """
#     # create data_folder if it doesn't exist
#     if not os.path.exists(data_folder):
#         os.makedirs(data_folder)
        
#     # set database fp
#     fp_database=os.path.join(data_folder,database_name)
    
#     # get normalised metadata_table_group_dict
#     metadata_table_dict = \
#         csvw_functions.validate_table_metadata(
#             metadata_document_location
#             )
#     print(metadata_table_dict)
    
#     table_name=metadata_table_dict['https://purl.org/berg/csvw_functions/vocab/table_name']['@value']
        
    
#     if _reload_database_table \
#         or not _check_if_table_exists_in_database(
#                 fp_database, 
#                 table_name
#                 ):
    
#         # import table data to database
#         _import_table_to_sqlite(
#                 metadata_table_dict,
#                 metadata_document_location,
#                 fp_database,
#                 verbose=verbose
#                 )



