import numpy as np

#Handling Missing Values
def handle_missing_values(df, strategy):
    if strategy == 'drop':
        clean_df = df.dropna()
    elif strategy in ['pad', 'bfill']:
        clean_df = df.fillna(method=strategy)
    else:
        raise ValueError("Invalid strategy. Choose from 'drop', 'pad', 'bfill'.")
    
    return clean_df

def handle_missing_values(df, strategy, column):
    if strategy == 'mean':
        clean_df = df.fillna(value = df[column].mean())
    elif strategy == 'max':
        clean_df = df.fillna(value = df[column].max())
    elif strategy == 'min':
        clean_df = df.fillna(value = df[column].min())
    else:
        raise ValueError("Invalid strategy. Choose from 'mean', 'max', 'min'.")
    
    return clean_df

def replace_missing_values(df, value):
    df2 = df.replace(to_replace = np.nan, value = value)
    
    return df2

def interpolate_missing_values(df):
    df2 = df.interpolate(method='linear')