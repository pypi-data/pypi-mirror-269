# -*- coding: utf-8 -*-

# remote csvw metadata functions
from .csvw_functions_extra import get_normalized_metadata_table_group_dict
from .csvw_functions_extra import get_available_csv_file_names

# download csv files
from .csvw_functions_extra import download_table_group

# downloaded csvw metadata file
from .csvw_functions_extra import get_metadata_table_group_dict
from .csvw_functions_extra import get_metadata_table_dict
from .csvw_functions_extra import get_metadata_column_dict
from .csvw_functions_extra import get_metadata_sql_table_names
from .csvw_functions_extra import get_metadata_columns_codes

# import_table_group_to_sqlite
from .csvw_functions_extra import import_table_group_to_sqlite

# database functions
from .csvw_functions_extra import add_index
from .csvw_functions_extra import get_all_table_names_in_database
from .csvw_functions_extra import get_sql_table_names_in_database
from .csvw_functions_extra import get_field_names
from .csvw_functions_extra import get_row_count
from .csvw_functions_extra import get_rows
from .csvw_functions_extra import run_sql

# utility functions
from .csvw_functions_extra import convert_to_iterator
from .csvw_functions_extra import get_field_string
from .csvw_functions_extra import get_group_by_string
from .csvw_functions_extra import get_where_string


