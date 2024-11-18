import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.impute import SimpleImputer


# Function for enconding categorial variables
def encode_categorical_variable(dataframe: pd.DataFrame, column_name: str, categories: list) -> None:
    '''
    Encodes a categorical variable in a pandas DataFrame using an ordinal encoder.

    Parameters:
        dataframe (pandas.DataFrame): The DataFrame containing the column to be encoded.
        column_name (str): The name of the column to be encoded.
        categories (list): The list of categories that the column can take.

    Returns:
        None: This function modifies the input DataFrame in place.
    '''
    # Create an ordinal encoder and fit to data
    encoder = OrdinalEncoder(categories=[categories])
    encoder.fit(dataframe[[column_name]])

    # Transform the data and replace the original column
    encoded_column = encoder.transform(dataframe[[column_name]]).astype(int)
    dataframe[column_name] = encoded_column
