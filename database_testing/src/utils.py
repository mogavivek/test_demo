import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_schema(df, expected_schema: dict):
    actual_schema = dict(df.dtypes.astype(str))
    
    for col, dtype in expected_schema.items():
        if col not in actual_schema or dtype not in actual_schema[col]:
            return False
    
    return True


def validate_not_null(df, not_null_cols:list):
    for col in not_null_cols:
        if df[col].isnull().any():
            return False
    return True


def yearly_order_drop_status(superstore_csv, db_result):
    """ CSV calculation"""
    superstore_csv["Year"] = (superstore_csv["Order Date"].astype(str).str.split("[/-]").str[-1].astype(int))
    
    csv_orders = superstore_csv.groupby("Year")["Order ID"].count().reset_index(name="total orders")
    csv_orders["pct_change"] = csv_orders["total orders"].pct_change().fillna(0).round(4)
    
    csv_status = dict(zip(csv_orders["Year"], csv_orders["pct_change"]))
    
    """ Microsoft SQL calculation """
    
    db_df = pd.DataFrame(db_result, columns=["year", "total_orders"])
    db_df["pct_change"] = db_df["total_orders"].pct_change().fillna(0).round(4)
    
    db_status = dict(zip(db_df["year"], db_df["pct_change"]))
    
    logger.info(f"CSV status is: {csv_status}")
    logger.info(f"DB status is: {db_status}")
    
    if csv_status == db_status:
        logger.info("Year over year growth stauts match (CSV vs DB)")
        return True
    else:
        logger.info("Mismatch found")
        return False