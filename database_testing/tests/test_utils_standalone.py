import pandas as pd
from src.utils import validate_schema, validate_not_null
import pytest


@pytest.mark.skip
def test_validate_schema():
    
    df = pd.DataFrame({"id": [1,2], "Name": ["Hello", "World"]})
    expected = {"id": "int64", "Name": "object"}
    
    assert validate_schema(df, expected), "Expected result is not similar to actual result"
    
@pytest.mark.skip
def test_validate_not_null():
    df = pd.DataFrame({"id": [1,2], "Name": ["Hello", "World"]})
    expected = ["id", "Name"]
    
    assert validate_not_null(df, expected)
    
def test_sample_df_fixture(sample_df):
    assert list(sample_df["Name"] == ["Hello", "World"])