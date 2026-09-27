import pandas as pd
import numpy as np
from logger import logger
from Load.database_loader import load_data
from Transform.transform import clean_amount, remove_empty_rows, clean_city
from validation.validate import (
    create_rejection_report,
    validate_amount,
    find_invalid_records,
    separate_records
)
from quarantine.quarantine import save_rejected_records
from config_loader import load_config


#load configuration
config = load_config()
file_path = config["input_file"]
logger.info("ETL process started")
# EXTRACT
try:
    df = pd.read_excel(file_path)
    logger.info("Data extraction completed")
except Exception as e:
    logger.error(f"Data extraction failed: {e}")
    print("ERROR:Could not extract data.")
    print(f"Reason:{e}")
    exit()

print("Before transformation:")
print(df)

# TRANSFORM
try:
    df = remove_empty_rows(df)
    df = clean_amount(df)
    df = clean_city(df)
    logger.info("Transformation completed")
except Exception as e:
    logger.error(f"Transformation failed: {e}")
    print("ERROR:Data transformation failed.")
    print(f"Reason:{e}")
    exit()

print("\nAfter transformation:")
print(df)

# VALIDATE
try:
    report = validate_amount(df)
    logger.info("Validation completed")
except Exception as e:
    logger.error(f"Validation failed: {e}")
    print("ERROR:Data validation failed.")
    print(f"Reason:{e}")
    exit()

print("\n DATA QUALITY REPORT")
for key, value in report.items():
    print(f"{key}: {value}")

valid_records, invalid_records = separate_records(df)

print("\nVALID RECORDS:")
print(valid_records)

print("\nINVALID RECORDS:")
print(invalid_records)

rejection_report = create_rejection_report(df)

print("\nREJECTION REPORT:")
print(rejection_report)
save_rejected_records(rejection_report)

#Load
try:
    load_data(valid_records, "sales")
    logger.info("Data loaded successfully")
except Exception as e:
    logger.error(f"Data loading failed: {e}")
    print("ERROR:Data loading failed.")
    print(f"Reason:{e}")
    exit()
    