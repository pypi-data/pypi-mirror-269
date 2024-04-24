import pandas as pd

# Data Reading
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def read_excel(file_path, sheet_name=0):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def read_json(file_path):
    df = pd.read_json(file_path)
    return df