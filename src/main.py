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

    #get subject id
    s_name = file.split('.')[0]
    s_id = constants.subject_id[s_name]

    #Add id of subject as an extra column
    temp_df.insert(9, "subject_id", s_id)

    #merge the dataframes
    homogeneous_df= pd.concat([homogeneous_df, temp_df])
    
    

#remove index columns from csv 21 & 15
print(homogeneous_df)