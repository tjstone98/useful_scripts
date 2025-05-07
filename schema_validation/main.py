import pandas as pd
import numpy as np
import glob, os, math, json, sys, re, warnings

warnings.filterwarnings('ignore', category=UserWarning)
###########################################
print('   ', '<'*3, '0.1: Environment Setup', '>'*3)
working_folder_PATH = r''

write_outputs = 'TRUE' # Set to FALSE for debugging.
##########################################################################################
def load_schema(schema_path):
    """
    Purpose: Load a schema JSON file.
    """
    with open(schema_path, 'r') as f:
        return json.load(f)
##########################################################################################
def validate_schema(dataframe, schema): 
    """
    Purpose: Validate DataFrame's schema.
    """
    schema_columns = schema["columns"]
    
    # Check if all expected columns are present
    if set(dataframe.columns) != set(schema_columns.keys()):
        if len(list(set(dataframe.columns) - set(schema_columns.keys()))) > 0:
            raise ValueError(f'Input columns do not match schema. These columns have been added: {list(set(dataframe.columns) - set(schema_columns.keys()))}.')
        if len(list(set(schema_columns.keys()) - set(dataframe.columns))) > 0:
            raise ValueError(f'Input columns do not match schema. These columns have been removed: {list(set(schema_columns.keys()) - set(dataframe.columns))}.')
        
    
    # Validate data types
    for col, expected_type in schema_columns.items():
        if expected_type == "string" and not pd.api.types.is_string_dtype(dataframe[col]):
            raise ValueError(f"Column '{col}' does not match expected type '{expected_type}'.")
        elif expected_type == "integer" and not pd.api.types.is_integer_dtype(dataframe[col]):
            raise ValueError(f"Column '{col}' does not match expected type '{expected_type}'.")
        elif expected_type == "float" and not pd.api.types.is_float_dtype(dataframe[col]):
            raise ValueError(f"Column '{col}' does not match expected type '{expected_type}'.")
        elif expected_type == "boolean" and not pd.api.types.is_bool_dtype(dataframe[col]):
            raise ValueError(f"Column '{col}' does not match expected type '{expected_type}'.")
        elif expected_type == "datetime" and not pd.api.types.is_datetime64_any_dtype(dataframe[col]):
            raise ValueError(f"Column '{col}' does not match expected type '{expected_type}'.")
##########################################################################################
def validate_file(file_path, schema_path):
    """
    Purpose: Load a file and validate its schema.
    """
    df = pd.read_csv(file_path)
    schema = load_schema(schema_path)
    validate_schema(df, schema)
##########################################################################################
def generate_monthly_schema(columns):
    """
    Purpose: Generate dynamic schema for rPRODv0003 and wPRODv0001.
    """
    schema = {
        "columns": {}
        }

    for col in columns:
        if pattern_store.match(col):
            schema['columns'][col] = 'object'
        elif pattern_sold_units.match(col):
            schema['columns'][col] = 'object' #'integer'
        elif pattern_sold_revenue.match(col):
            schema['columns'][col] = 'object' #'float'
        elif pattern_sold_profit.match(col):
            schema['columns'][col] = 'object' #'float'
    return schema
##########################################################################################
# Import dataframe (can be CSV, XLSX, etc.) and schema (must be JSON).
try:
    validate_schema(
        dataframe = df,
        schema = load_schema()
    )
    print('Validation passed.')
except ValueError as e:
    print(f'Validation failed: {e}')
    sys.exit(1) # This will kill the script if validation fails.
