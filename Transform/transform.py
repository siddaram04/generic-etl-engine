import pandas as pd
def remove_empty_rows(df):
    df = df.dropna(how="all")
    return df
def clean_amount(df):
    df["Amount"] = df["Amount"].astype(str).str.replace('"', '', regex=False).str.strip()
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    return df

def clean_city(df):
    df["City"] = df["City"].str.strip().str.title()
    return df