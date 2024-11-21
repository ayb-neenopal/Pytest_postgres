import pytest
from product_pipeline import extract, load

def run_pipeline():
    # Step 1: Extract data
    df, tbl_name = extract()

    # Step 2: Run tests
    print("Running tests...")
    result = pytest.main(["-q", "--disable-warnings", "test_product.py"])
    
    # Abort pipeline if any test fails
    if result != 0:
        print("Tests failed. Aborting the pipeline.")
        return  # Stop further execution
    
    print("Tests passed! Proceeding to load data...")
    load(df, tbl_name)

if __name__ == "__main__":
    run_pipeline()
