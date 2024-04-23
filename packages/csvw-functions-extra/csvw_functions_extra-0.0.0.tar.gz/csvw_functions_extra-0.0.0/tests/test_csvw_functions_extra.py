# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 14:49:13 2023

@author: cvskf
"""
import unittest

import csvw_functions
import csvw_functions_extra 
import os

fp_table_group_metadata='extra_tables-metadata.json'

class EXTRA(unittest.TestCase):
    ""
        
    def _test_download_table_group(self):
        ""
        
        csvw_functions_extra.download_table_group(
            metadata_document_location=fp_table_group_metadata,
            data_folder='_data',
            csv_file_names='Local_Authority_District_to_Region_December_2022.csv',
            overwrite_existing_files=True,
            verbose=True
            )
        
        
    def _test_import_table_group_to_sqlite(self):
        ""
        
        csvw_functions_extra.import_table_group_to_sqlite(
            metadata_filename='extra_tables-metadata.json',
            data_folder='_data',
            database_name='data.sqlite',
            csv_file_names='Local_Authority_District_to_Region_December_2022.csv',
            overwrite_existing_tables=True,
            verbose=True
            )
        
        
class TESTUtilityFunctions(unittest.TestCase):
    ""
    
    def test_convert_to_iterator(self):
        ""
        # None
        result = \
            csvw_functions_extra.convert_to_iterator(
                None
                )
        self.assertEqual(
            result,
            []
            )
        
        # int
        result = \
            csvw_functions_extra.convert_to_iterator(
                1
                )
        self.assertEqual(
            result,
            [1]
            )
        
        # list
        result = \
            csvw_functions_extra.convert_to_iterator(
                [1,2]
                )
        self.assertEqual(
            result,
            [1,2]
            )
        
        # str
        result = \
            csvw_functions_extra.convert_to_iterator(
                'abc'
                )
        self.assertEqual(
            result,
            ['abc']
            )
        
        
    def test_get_field_string(self):
        ""
        # None
        result = \
            csvw_functions_extra.get_field_string(
                None
                )
        self.assertEqual(
            result,
            '*'
            )
        
        # str
        result = \
            csvw_functions_extra.get_field_string(
                'field1'
                )
        self.assertEqual(
            result,
            ' "field1" '
            )
        
        
        # list
        result = \
            csvw_functions_extra.get_field_string(
                [
                    'field1',
                    'field2'
                    ]
                )
        self.assertEqual(
            result,
            ' "field1","field2" '
            )
        
        
    def test_get_group_by_string(self):
        ""
        # None
        result = \
            csvw_functions_extra.get_group_by_string(
                None
                )
        self.assertEqual(
            result,
            ('', '')
            )
        
        # str
        result = \
            csvw_functions_extra.get_group_by_string(
                'field1'
                )
        self.assertEqual(
            result,
            (' "field1", ', 'GROUP BY "field1" ')
            )
        
        # list
        result = \
            csvw_functions_extra.get_group_by_string(
                [
                    'field1',
                    'field2'
                    ]
                )
        self.assertEqual(
            result,
            (' "field1","field2", ', 'GROUP BY "field1","field2" ')
            )
        
        
    def test_get_where_string(self):
        ""
        # None
        result = \
            csvw_functions_extra.get_where_string(
                None
                )
        self.assertEqual(
            result,
            ''
            )
        
        # dict, single item single value
        result = \
            csvw_functions_extra.get_where_string(
                {
                    'field1': 1
                    }
                )
        self.assertEqual(
            result,
            ' WHERE ("field1" = 1)'
            )
        
        # dict, three values single value
        result = \
            csvw_functions_extra.get_where_string(
                {
                    'field1': 1,
                    'field2': 'a',
                    'field3': None
                    }
                )
        self.assertEqual(
            result,
            ' WHERE ("field1" = 1) AND ("field2" = "a") AND ("field3" = Null)'
            )
        
        # dict, single item two integers
        result = \
            csvw_functions_extra.get_where_string(
                {
                    'field1': [1,2]
                    }
                )
        self.assertEqual(
            result,
            ' WHERE ("field1" IN (1,2))'
            )
        
        # dict, single item two strings
        result = \
            csvw_functions_extra.get_where_string(
                {
                    'field1': ['a','b']
                    }
                )
        self.assertEqual(
            result,
            ' WHERE ("field1" IN ("a","b"))'
            )
        
        # dict, BETWEEN integers
        result = \
            csvw_functions_extra.get_where_string(
                {
                    'field1': {
                        'BETWEEN':[1,2]
                        }
                    }
                )
        self.assertEqual(
            result,
            ' WHERE ("field1" BETWEEN (1 AND 2))'
            )
        
        # dict, BETWEEN strings
        result = \
            csvw_functions_extra.get_where_string(
                {
                    'field1': {
                        'BETWEEN':['a','b']
                        }
                    }
                )
        self.assertEqual(
            result,
            ' WHERE ("field1" BETWEEN ("a" AND "b"))'
            )
        
        
        
if __name__=="__main__":
    
    unittest.main()

