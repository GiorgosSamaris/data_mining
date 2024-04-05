import pandas as pd
import os 
import plotter
import constants
from utilities import CSVHandler as csv
from utilities import Preprocessing as preproc
import matplotlib.pyplot as plt
import datetime

def read_data(folder_path = ".",preproc = False) -> pd.DataFrame:
    homogeneous_df = pd.DataFrame()
    for file in os.listdir(constants.CSV_PATH):
        temp_df = csv.read_csv(file)
        if temp_df is None:
            continue
        if(preproc):
            temp_df = preproc.drop_nonuniform_columns(temp_df)
            temp_df = preproc.add_subject_id(temp_df, file, 8)
        homogeneous_df= pd.concat([homogeneous_df, temp_df])
    return homogeneous_df        

def main():
    df = pd.read_csv(constants.CSV_PATH + "S006.csv")
    df = preproc.drop_dates(data_frame=df)
    df = preproc.convert_to_seconds(data_frame=df)
    # plt.plot(df["timestamp"], df["back_x"])
    # plt.show()
    if(constants.PROCESS):
        merged_df = read_data(constants.CSV_PATH, preproc=False)
        if not os.path.exists(constants.PROCESSED_CSV_PATH):
            print("process folder does not exist, creating...")
            # If it doesn't exist, create it
            os.makedirs(constants.PROCESSED_CSV_PATH)
        #convert data to csv
        merged_df.to_csv(constants.PROCESSED_CSV_PATH + "proc_merged.csv")
    if(constants.GRAPH):
        merged_df = pd.read_csv(constants.PROCESSED_CSV_PATH + "proc_merged.csv")
        plotter.plot_gyro(merged_df)
        # back_sensor_df, thigh_sensor_df = preproc.separate_sensors(merged_df)
        # plot_data = back_sensor_df.loc[:,["timestamp","back_x"]]

if __name__ == "__main__":
    main()