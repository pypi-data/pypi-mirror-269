# Data Summaries
def mean(df):
    return df.mean()

def standardDeviation(df):
    return df.std()

def count(df):
    return df.count()

def min(df):
    return df.min()

def max(df):
    return df.max()

def frequent_values(df):
    return df.value_counts()

def summary(df):
    return df.describe()