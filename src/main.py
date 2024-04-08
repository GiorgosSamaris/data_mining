import pandas as pd
import os 
import plotter
import constants
from utilities import CSVHandler as csv
from utilities import Preprocessing as preproc
import matplotlib.pyplot as plt
import datetime

def read_data(preprocess = False) -> pd.DataFrame:
    homogeneous_df = pd.DataFrame()
    for file in os.listdir(constants.CSV_PATH):
        temp_df = csv.read_csv(file)
        if temp_df is None:
            continue
        if(preprocess):
            temp_df = preproc.drop_nonuniform_columns(temp_df)
            temp_df = preproc.add_subject_id(temp_df, file, 8)
        homogeneous_df= pd.concat([homogeneous_df, temp_df])
    return homogeneous_df        

def main():
    df = pd.read_csv(constants.CSV_PATH + "S006.csv")
    df = preproc.drop_dates(data_frame=df)
    df = preproc.convert_to_seconds(data_frame=df)
    df = preproc.add_subject_id(data_frame=df, file_name="S006.csv", column_pos=8)
    df_windowed = preproc.window_data(df_input=df, window_size=200)

    ax = plt.subplot()
    plotter.plot_timeseries()
    plotter.plot_timeseries(df,"back_x",axes=ax)
    plotter.plot_timeseries(df,"back_y",axes=ax)
    plotter.plot_timeseries(df,"back_z",axes=ax)
    plt.show()
    # plotter.activity_histogram(df_windowed)
    # plotter.activity_histogram(df)
    # if(constants.PROCESS):
    #     merged_df = read_data(preprocess=False)
    #     if not os.path.exists(constants.PROCESSED_CSV_PATH):
    #         print("process folder does not exist, creating...")
    #         os.makedirs(constants.PROCESSED_CSV_PATH)
    #     merged_df.to_csv(constants.PROCESSED_CSV_PATH + "proc_merged.csv")
    # if(constants.GRAPH):
    #     merged_df = pd.read_csv(constants.PROCESSED_CSV_PATH + "proc_merged.csv")
    #     plotter.plot_gyro(merged_df)

if __name__ == "__main__":
    main()