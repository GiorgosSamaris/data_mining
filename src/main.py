import pandas as pd
import os 
import matplotlib as plt
import constants
import csv_handler
homogeneous_df = pd.DataFrame()



for file in os.listdir(constants.CSV_PATH):
    temp_df = csv_handler.read_csv(file)
    
    if temp_df is None:
        continue
  
    temp_df = csv_handler.drop_nonuniform_columns(temp_df)
    #Check for outliers by calculating IQR for each column
    temp_df = csv_handler.drop_outliers(temp_df)

    #Seperate sensor data 
    back_df, thigh_df = csv_handler.seperate_sensors(temp_df)

    print(back_df)
    #Data bining
    # csv_handler.data_binning(temp_df)
    # homogeneous_df= pd.concat([homogeneous_df, temp_df])

#remove index columns from csv 21 & 15
print(homogeneous_df.shape)