import pandas as pd
import os 
import matplotlib as plt


csv_path = "../harth/harth/"
txt_output_path = "./output.txt"

homogeneous_df = pd.DataFrame()



for file in os.listdir(csv_path):

    #skip git ignore
    if file == ".gitignore":
        continue
        

    temp_df = pd.read_csv(csv_path + file)

    print("---------------------------------------------------------------------------------------------\n")

    print("File: {}".format(file))


    # Exploratory data analysis
    print(temp_df.head())
    print(temp_df.describe())
    print(temp_df.info())

    print("Missing values: {}".format(temp_df.isnull().sum()))

    # Remove useless columns
    if "index" in temp_df.columns:
        temp_df.drop(['index'], axis='columns', inplace=True)  
        print("Removed column 'index'")

    if "Unknown: 0" in temp_df.columns:
        temp_df.drop(['Unknown: 0'], axis='columns', inplace=True)  
        print("Removed column 'Unknown: 0'")

    print("Size of file before dropping outliers: {}".format(temp_df.shape))

    #Check for outliers by calculating IQR for each column
    for column in ['back_x','back_y','back_z','thigh_x','thigh_y','thigh_z']:
        
        Q1 = temp_df[column].quantile(0.25)
        Q3 = temp_df[column].quantile(0.75)


        IQR = Q3 - Q1

        threshold = 1.5

        # outliers = temp_df[(temp_df[column] < Q1 - threshold * IQR) | (temp_df[column] > Q3 + threshold * IQR)]
        temp_df[(temp_df[column] < Q1 - threshold * IQR) | (temp_df[column] > Q3 + threshold * IQR)] = temp_df[column].median()

        # drop rows containing outliers
        # temp_df = temp_df.drop(outliers.index)


    #Data bining
        


        
    # homogeneous_df= pd.concat([homogeneous_df, temp_df])
    print("Size of file after dropping outliers: {}".format(temp_df.shape))
    print()


#remove index columns from csv 21 & 15

print(homogeneous_df.shape)