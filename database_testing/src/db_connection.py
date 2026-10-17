import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBConnection:
    
    def __init__(self, server, driver, user=None, password=None):
        
        try:
            odbc_string = (f"DRIVER={{{driver}}};"
                           f"SERVER={server};"
                           "DATABASE=master;")
            
            if user and password:
                odbc_string = odbc_string + (f"UID={user};"
                                             f"PWD={password};")
            else:
                odbc_string = odbc_string + "Trusted_Connection=yes;"
            
            conn_string = ("mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_string))
            self.engine = create_engine(conn_string)
            
            # Test the connection
            
            with self.engine.connect() as conn:
                conn.execute(text("select 1"))
            
            logger.info("Connected to Microsoft SQL Server")
        
        except SQLAlchemyError as e:
            logger.info("Connection Error: ", e)
            self.engine = None
    
    def run_query(self, query, params=None):
        if self.engine is None:
            logger.info("No active DB connection")
            return None
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                
                if result.returns_rows:
                    return result.fetchall()
                
                return None
        
        except SQLAlchemyError as e:
            print("Query Error:", e)
            return None
        
    
    def close(self):
        if self.engine:
            self.engine.dispose()
            logger.info("Connection Closed")

# server_name = os.getenv("SERVER")
# driver_name = os.getenv("DRIVER")
# query = "select top 5 * from dbo.superstore_data where ship_mode = 'Second Class'"

# db = DBConnection(server_name, driver_name)
# print(db.run_query(query))
# db.close()