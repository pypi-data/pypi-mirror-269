import numpy as np

#Handling Missing Values
def handle_missing_values(data, strategy):
    if strategy == 'drop':
        clean_data = data.dropna()
    elif strategy in ['mean', 'median', 'mode']:
        clean_data = data.fillna(data.agg(strategy))
    elif strategy in ['ffill', 'bfill']:
        clean_data = data.fillna(method=strategy)
    else
        raise ValueError("Invalid strategy. Choose from 'drop', 'mean', 'median', 'mode', 'ffill', 'bfill'.")
    
    return clean_data

def replace_missing_values(data, newValue):
    clean_data = data.replace(to_replace = np.nan, value = newValue)
    
    return clean_data