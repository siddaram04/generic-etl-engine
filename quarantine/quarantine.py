import os


def save_rejected_records(df):

    os.makedirs("quarantine", exist_ok=True)

    file_path = "quarantine/rejected_records.csv"

    df.to_csv(file_path, index=False)

    print(f"Rejected records saved to: {file_path}")