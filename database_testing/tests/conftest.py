import sys
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

import pandas as pd
import pytest
from src.db_connection import DBConnection

load_dotenv()

# Project root: parent of the tests directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

file_path = os.getenv("FILE_PATH")
server_name = os.getenv("SERVER")
driver_name = os.getenv("DRIVER")
test_path = os.getenv("TEST_PATH")


# Below is just created for the example
# @pytest.fixture(scope="session")
# def sample_df():
#    print("Creating sample DataFrame")
#    return pd.DataFrame({"id": [1,2], "Name": ["Hello", "World"]})

@pytest.fixture(scope="session")
def db():
    """Connection to the DB"""
    conn = DBConnection(
        server=server_name,
        driver=driver_name
    )
    
    yield conn
    
    conn.close()
    
    
@pytest.fixture(scope="session")
def load_superstore_csv():
    """ load superstore csv """
    return pd.read_csv(file_path, encoding="latin1")

@pytest.fixture(scope="session")
def test_cases_file():
    """ load Excel driven test cases """
    return pd.read_excel(test_path)