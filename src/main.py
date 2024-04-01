import pandas as pd
import os 
import plotter
import constants
import csv_handler
homogeneous_df = pd.DataFrame()

for file in os.listdir(constants.CSV_PATH):
    temp_df = csv_handler.read_csv(file)
    if temp_df is None:
        continue
    temp_df = csv_handler.drop_nonuniform_columns(temp_df)
    #Check for outliers by calculating IQR for each column
    # temp_df = csv_handler.drop_outliers(temp_df)
    subject_name = file.split('.')[0]
    subject_id = constants.subject_id[subject_name]
    temp_df['subject_id'] = subject_id
    print(temp_df.head(1))
    # plotter.activity_pie(temp_df)
    plotter.activity_histogram(temp_df)
    input("Enter to continue...")
    homogeneous_df= pd.concat([homogeneous_df, temp_df])

print(homogeneous_df.head(0))