from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Data Encoding
def encode_categorical(data, by, strategy):
    if strategy == 'one-hot':
        data_passthrough = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [by])], remainder='passthrough')
        data_encoded = np.array(data_passthrough.fit_transform(data))
    elif strategy == 'label':
        data_encoded = LabelEncoder().fit_transform(data[by])

    return data_encoded
