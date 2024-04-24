import numpy as np

#Handling Missing Values
def handle_missing_values(data, strategy):
    if strategy == 'drop':
        data_cleaned = data.dropna()
    elif strategy in ['mean', 'median', 'mode']:
        data_cleaned = data.fillna(data.agg(strategy))
    elif strategy in ['ffill', 'bfill']:
        data_cleaned = data.fillna(method=strategy)
    else:
        raise ValueError("Invalid strategy. Choose from 'mean', 'median', 'mode', 'ffill', 'bfill', 'drop'.")
    
    return data_cleaned

def replace_missing_values(data, newValue):
    clean_data = data.replace(to_replace = np.nan, value = newValue)
    
    return clean_data