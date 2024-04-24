from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


# Data Encoding
def encode_categorical(data, by, strategy):
    if strategy == 'one-hot':
        df_encoded = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [by])], remainder='passthrough')
        df_transformed = np.array(df_encoded.fit_transform(data))
        return df_transformed
    elif strategy == 'label':
        df_encoded = LabelEncoder().fit_transform(data[by])
        return df_encoded
    
    return df_transformed
