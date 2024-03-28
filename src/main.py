import pandas as pd
import os 
import matplotlib as plt
import constants
import csv_handler
homogeneous_df = pd.DataFrame()



for file in os.listdir(constants.CSV_PATH):
    temp_df = csv_handler.read_csv(file, True)
    if temp_df.isnull():
        continue
    temp_df = csv_handler.drop_nonuniform_columns(temp_df)
    #Check for outliers by calculating IQR for each column
    temp_df = csv_handler.drop_outliers(temp_df)
    #Data bining
    # homogeneous_df= pd.concat([homogeneous_df, temp_df])

#remove index columns from csv 21 & 15
print(homogeneous_df.shape)