import os
import pandas as pd
from sqlalchemy import create_engine
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ This function clean the columns name and all"""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    
    return df

def load_csv_to_microsoftsql(csv_file, table_name, conn_string):
    df = pd.read_csv(csv_file, encoding="latin1")
    clean_df = clean_columns(df)
    engine = create_engine(conn_string)
    engine = engine.connect()
    clean_df.to_sql(table_name, engine, if_exists="replace", index=False)
    logger.info(f"{len(df)} records are loaded successfully into table {table_name}")


# file_path = os.getenv("FILE_PATH")
# server_name = os.getenv("SERVER")
# driver_name = os.getenv("DRIVER")

# csv_file = file_path
# conn_string = 'mssql://' + server_name + '/master?driver=' + driver_name
# load_csv_to_microsoftsql(csv_file, "superstore_data", conn_string)



