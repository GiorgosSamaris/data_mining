import pandas as pd
import os 
import matplotlib as plt


csv_path = "../harth/harth/"

homogeneous_df = pd.DataFrame()
for file in os.listdir(csv_path):
    temp_df = pd.read_csv(csv_path + file)

    print("---------------------------------------------------------------------------------------------\n")

    print("File: {}".format(file))

    # Remove useless columns
    # if "index" in temp_df.columns:
    #     temp_df.drop(['index'], axis='columns', inplace=True)  
    #     print("Removed column 'index'")

    # if "Unknown: 0" in temp_df.columns:
    #     temp_df.drop(['Unknown: 0'], axis='columns', inplace=True)  
    #     print("Removed column 'Unknown: 0'")
    
    # Exploratory data analysis
    print(temp_df.head())
    print(temp_df.describe())
    print(temp_df.info())

    prev_size = temp_df.shape[0]
    temp_df.drop_duplicates(inplace=True, subset=['timestamp'])
    curr_size = temp_df.shape[0]
    print("Removed : ", str(prev_size - curr_size), " duplicates")
    homogeneous_df= pd.concat([homogeneous_df, temp_df])
    print()


#remove index columns from csv 21 & 15

print(homogeneous_df.shape)