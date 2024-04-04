import numpy as np
# separate classes of each dataframe to new dataframe
def separate_activities(data_frame):
    """
    Separate classes of each dataframe to new dataframe

    Parameters:
        data_frame (pandas.DataFrame): The DataFrame to be separated.

    Returns:
        dict : A dictionary containing the separated dataframes.
    """
    separated_data = {}
    for i in np.unique(data_frame['label']):
        separated_data[i] = data_frame[data_frame['label'] == i]
    return separated_data