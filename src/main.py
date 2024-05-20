import pandas as pd
import os 
import plotter
from classification import Classifiers 
import constants
from utilities import CSVHandler as csv
from utilities import Preprocessing as preproc
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

import numpy as np
def read_data(file_path = ".") -> dict[pd.DataFrame]:
    dataframes = {}
    
    for file in os.listdir(file_path):
        temp_df = csv.read_csv(file_path+file)
        if temp_df is None:
            continue
        
        dataframes[file] = temp_df

    return dataframes




def main():
    dataframes_dict = read_data(constants.CSV_PATH)
    homogeneous_df = pd.DataFrame()
    for key in dataframes_dict:
        df = dataframes_dict[key]       
        if constants.OPTIONS & 1 == constants.DROP_DATES:
            df = preproc.drop_dates(data_frame=df)
        if constants.OPTIONS & 2 == constants.TO_SEC:
            df = preproc.convert_to_seconds(data_frame=df)
        if constants.OPTIONS & 4 == constants.ADD_SUBJECT_ID:
            df = preproc.add_subject_id(data_frame=df, file_name = key, column_pos=8)
        if constants.OPTIONS & 8 == constants.WINDOW_DATA:
            df = preproc.window_data(df_input=df, window_size=200)
        if constants.OPTIONS & 16 == constants.WRITE_DATA:
            pass
        if constants.OPTIONS & 32 == constants.DROP_NON_UNIFORM_COLUMNS:
            df = preproc.drop_nonuniform_columns(df)
        if constants.OPTIONS & 64 == constants.MERGE:
            homogeneous_df = pd.concat([homogeneous_df, df])

    
    X = homogeneous_df[["thigh_x", 'back_x', 'thigh_y', 'back_y', 'thigh_z', 'back_z', 'variance_back_x', 'variance_back_y', 'variance_back_z', 'variance_thigh_x', 'variance_thigh_y', 'variance_thigh_z']]
    Y = homogeneous_df[["label"]]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
    # model = GaussianNB()
    # model = RandomForestClassifier()
    model = MLPClassifier()
    print(Classifiers.get_metrics(model,X_train,X_test,y_train,y_test))
if __name__ == "__main__":
    main()