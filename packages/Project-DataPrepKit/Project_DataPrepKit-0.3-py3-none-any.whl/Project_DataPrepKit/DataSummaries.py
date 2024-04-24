# Data Summaries
def mean(data):
    return np.mean(data)

def median(data):
    return np.median(data)

def mode(data):
    return data.mode().values.tolist()

def standardDeviation(data):
    return np.std(data)

def min(data):
    return np.min(data)

def max(data):
    return np.max(data)

def frequent_values(data):
    return data.value_counts()

def summary(data):
        summary = {
        'mean': np.mean(data),
        'median': np.median(data),
        'mode': data.mode().iloc[0],  # Get the first mode if multiple exist
        'min': np.min(data),
        'max': np.max(data),
        'std_dev': dnp.std(data),
        'num_missing_values': data.isnull().sum(),
    }