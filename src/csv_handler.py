import pandas as pd
import constants

def read_csv(input_file, verbose = False):
    """
    Read a CSV file and return its contents as a pandas DataFrame.
    Parameters:
        input_file (str): The path to the CSV file to be read.
        verbose (bool, optional): If True, print additional information about the DataFrame such as head, description, info, and missing values. Default is False.
    Returns:
        pandas.DataFrame or None: The DataFrame containing the CSV data if the file exists and is not ".gitignore", otherwise returns None.
    """
    if input_file == ".gitignore":
        return None
    csv_data_frame = pd.read_csv(constants.CSV_PATH + input_file)
    if verbose:
        print("---------------------------------------------------------------------------------------------\n")
        print("File: {}".format(input_file))
        print(csv_data_frame.head())
        print(csv_data_frame.describe())
        print(csv_data_frame.info())
        print("Missing values: {}".format(csv_data_frame.isnull().sum()))
    return csv_data_frame 

def drop_nonuniform_columns(data_frame, verbose=False):
    """
    Drop columns 'index' and 'Unknown: 0' from the DataFrame if they exist.

    Parameters:
        data_frame (pandas.DataFrame): The DataFrame from which columns are to be dropped.
        verbose (bool, optional): If True, print a message for each column dropped. Default is False.

    Returns:
        None
    """
    if "index" in data_frame.columns:
        data_frame.drop(['index'], axis='columns', inplace=True)
        if verbose:
            print("Removed column 'index'")

    if "Unknown: 0" in data_frame.columns:
        data_frame.drop(['Unknown: 0'], axis='columns', inplace=True)
        if verbose:
            print("Removed column 'Unknown: 0'")
    return None

def drop_outliers(data_frame, verbose = False):
    """
    Drop outliers from specific columns of the DataFrame using the IQR method.

    Parameters:
        data_frame (pandas.DataFrame): The DataFrame from which outliers are to be dropped.
        verbose (bool, optional): If True, print the size of the DataFrame before and after dropping outliers. Default is False.

    Returns:
        None
    """
    if verbose:
        print("Size of file before dropping outliers: {}".format(data_frame.shape))
    for column in ['back_x','back_y','back_z','thigh_x','thigh_y','thigh_z']:
        Q1 = data_frame[column].quantile(0.25)
        Q3 = data_frame[column].quantile(0.75)
        IQR = Q3 - Q1
        threshold = 1.5
        # outliers = data_frame[(data_frame[column] < Q1 - threshold * IQR) | (data_frame[column] > Q3 + threshold * IQR)]
        data_frame[(data_frame[column] < Q1 - threshold * IQR) | (data_frame[column] > Q3 + threshold * IQR)] = data_frame[column].median()
        # drop rows containing outliers
        # data_frame = data_frame.drop(outliers.index)
    if verbose:
        print("Size of file after dropping outliers: {}".format(data_frame.shape))