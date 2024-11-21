import pytest
import pandas as pd
from product_pipeline import extract

# Fixture to extract the data for testing
@pytest.fixture(scope="module")
def extracted_data():
    """
    Extract data from the pipeline for testing.
    Returns:
        tuple: DataFrame and table name from the extraction step.
    """
    df, tbl_name = extract()
    return df, tbl_name

# Test to check if 'ProductKey' column exists
def test_col_exists(extracted_data):
    df, _ = extracted_data
    assert 'ProductKey' in df.columns, "Column 'ProductKey' is missing from the data."

# Test to check if 'ProductKey' column has no null values
def test_null_check(extracted_data):
    df, _ = extracted_data
    assert df['ProductKey'].notnull().all(), "'ProductKey' contains null values."

# Test for uniqueness in 'ProductKey' column
def test_unique_check(extracted_data):
    df, _ = extracted_data
    assert df['ProductKey'].is_unique, "'ProductKey' contains duplicate values."

# Test for correct data type of 'ProductKey'
def test_productkey_dtype_int(extracted_data):
    df, _ = extracted_data
    assert pd.api.types.is_integer_dtype(df['ProductKey']), "'ProductKey' is not of integer type."

# Test for correct data type of 'EnglishProductName'
def test_productname_dtype_str(extracted_data):
    df, _ = extracted_data
    assert pd.api.types.is_object_dtype(df['EnglishProductName']), "'EnglishProductName' is not of string type."

# Test for checking if 'SafetyStockLevel' values are in the correct range
def test_range_val(extracted_data):
    df, _ = extracted_data
    assert df['SafetyStockLevel'].between(0, 1000).all(), "'SafetyStockLevel' values are out of range (0-1000)."

# Test to check valid values for the 'Color' column
def test_color_values(extracted_data):
    df, _ = extracted_data
    valid_colors = {'NA', 'Black', 'Slver', 'Red', 'White', 'Blue', 'Multi', 'Yellow', 'Grey', 'Silver/Black'}
    invalid_colors = set(df['Color'].unique()) - valid_colors
    assert not invalid_colors, f"Invalid color values found: {invalid_colors}"
