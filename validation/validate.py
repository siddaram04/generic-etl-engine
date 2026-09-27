import pandas as pd


def validate_amount(df):
    missing_amount=df["Amount"].isna().sum()
    negative_amount=(df["Amount"] < 0).sum()

    print("missing Amount:",missing_amount)
    print("negative Amount:",negative_amount)

    report={}
    report["total_records"]=len(df)
    report["missing_customer"]=df["customer"].isna().sum()
    report["missing_amount"]=df["Amount"].isna().sum()
    report["negative_amount"]=(df["Amount"] < 0).sum()
    report["missing_city"]=df["City"].isna().sum()
    report["duplicate_records"]=df.duplicated().sum()
    return report


def find_missing_city_records(df):
    return df[df["city"].isna()]

def find_invalid_records(df):

    invalid = (
        df["Amount"].isna()
        | (df["Amount"] < 0)
    )

    invalid_records = df[invalid]

    return invalid_records

def separate_records(df):

    invalid = (
        df["Amount"].isna()
        | (df["Amount"] < 0)
    )

    invalid_records = df[invalid]

    valid_records = df[~invalid] # ~ means not

    return valid_records, invalid_records

def create_rejection_report(df):

    records = []

    for index, row in df.iterrows():
        if pd.isna(row["Amount"]):

            records.append({
                "customer": row["customer"],
                "Amount": row["Amount"],
                "City": row["City"],
                "rejection_reason": "Missing Amount"
            })

        elif row["Amount"] < 0:

            records.append({
                "customer": row["customer"],
                "Amount": row["Amount"],
                "City": row["City"],
                "rejection_reason": "Negative Amount"
            })

    return pd.DataFrame(records)