import pandas as pd
import os 
import matplotlib.pyplot as plt
import constants
import csv_handler


def read_data(folder_path = ".",preproc = False) -> pd.DataFrame:
    
    homogeneous_df = pd.DataFrame()
    for file in os.listdir(constants.CSV_PATH):
        temp_df = csv_handler.read_csv(file)
        if temp_df is None:
            continue


        if(preproc):
            temp_df = csv_handler.drop_nonuniform_columns(temp_df)
            # #Check for outliers by calculating IQR for each column
            # temp_df = csv_handler.drop_outliers(temp_df)//    

            #Add a column describing subject id
            temp_df = csv_handler.add_subject_id(temp_df, file, 8)

        #merge the dataframes
        homogeneous_df= pd.concat([homogeneous_df, temp_df])

    return homogeneous_df        
    






def main():

    if(constants.PROCESS):
        merged_df = read_data(constants.CSV_PATH, preproc=True)

        #convert data to csv
        merged_df.to_csv(constants.PROC_CSV_PATH + "proc_merged.csv")

    if(constants.GRAPH):
        merged_df = pd.read_csv(constants.PROC_CSV_PATH + "proc_merged.csv")

        # back_sensor_df, thigh_sensor_df = csv_handler.separate_sensors(merged_df)

        # plot_data = back_sensor_df.loc[:,["timestamp","back_x"]]


if __name__ == "__main__":
    main()