from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


# Data Encoding
def encode_categorical(df, columns):
    df_encoded = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
    
    return df_encoded