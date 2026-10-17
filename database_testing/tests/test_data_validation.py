import pytest
import pandas as pd
from dotenv import load_dotenv
import os
import logging
import json
from src.utils import validate_not_null, yearly_order_drop_status

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

test_path = os.getenv("TEST_PATH")

def run_validation(testcase, superstore_csv, db):
    query_logic = testcase["Query / Logic"]
    expected = testcase["ExpectedValue"]
    
    if query_logic.startswith("SELECT"):
        db_result = db.run_query(query_logic)
        
        if expected == "csv_count":
            return db_result[0][0] == len(superstore_csv)
        
        elif expected.startswith("csv_groupby:"):
            col = expected.split(":")[1]
            csv_result = superstore_csv.groupby(col)["Order ID"].count().reset_index().values.tolist()
            db_result = [list(row) for row in db_result]
            return sorted(db_result) == sorted(csv_result)
        
        elif expected.startswith("csv_groupby_year:"):
            col = expected.split(":")[1]
            if col == "Order ID":
                csv_result = superstore_csv.groupby(pd.to_datetime(superstore_csv["Order Date"]).dt.year)["Order ID"].count().to_dict()
                db_dict = {int(k): v for k, v in db_result}
            else:
                csv_result = superstore_csv.groupby(pd.to_datetime(superstore_csv["Order Date"]).dt.year)["Profit"].sum().round(2).to_dict()
                db_dict = {int(k): round(v, 2) for k, v in db_result}
            
            return db_dict == csv_result
        
        elif testcase["TestCaseName"].startswith("Schema"):
            
            db_schema = {col.lower().replace(" ", "_"): dtype.lower().replace(" ", "_") for col, dtype in db_result}
            logger.info(f"Actual schema (db): {db_schema}")

            
            logger.info(f"The expected is: {expected}")
            expected_schema = json.loads(expected)            
            expected_schema = {col.lower().replace(" ", "_"): dtype.lower().replace(" ", "_") for col, dtype in expected_schema.items()}
            logger.info(f"Expected schema (db): {expected_schema}")
            
            type_mapping = {
                "text": "varchar",
                "double_precision": "float"
            }
            for col, dtype in expected_schema.items():
                expected_schema[col] = type_mapping.get(dtype, dtype)
            
            for col, dtype in expected_schema.items():
                if col not in db_schema:
                    logger.info(f"Column missing in DB: {col}")
                    return False
                if db_schema[col] != dtype:
                    logger.info(f"Type missing in {col}: expected {dtype}, got {db_schema[col]}")
                    return False
            
            logger.info("Schema validation passed (Excel vs db)")
            return True
        
        elif testcase["TestCaseName"].startswith("% of Orders"):
            return yearly_order_drop_status(superstore_csv, db_result)

    elif query_logic.startswith("CHECK_NOT_NULL"):
        not_null_cols = json.loads(expected)
        return validate_not_null(superstore_csv, not_null_cols)
    
    return False


@pytest.mark.parametrize("testcase", [pytest.param(tc, id=tc["TestCaseName"]) for _,tc in pd.read_excel(test_path, sheet_name="Sheet1").iterrows()])
def test_data_validation(testcase, load_superstore_csv, db):
    assert run_validation(testcase, load_superstore_csv, db), f"Failed: {testcase}"