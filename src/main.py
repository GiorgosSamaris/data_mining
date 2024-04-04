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
            # #Check for outliers by calculating IQR for each column
            # temp_df = preproc.drop_outliers(temp_df)//    

            #Add a column describing subject id
            temp_df = preproc.add_subject_id(temp_df, file, 8)

        #merge the dataframes
        homogeneous_df= pd.concat([homogeneous_df, temp_df])

    return homogeneous_df        
    






def main():


    df = pd.read_csv(constants.CSV_PATH + "S006.csv")

    df = preproc.drop_dates(data_frame=df)

    print(df)

    # plt.plot(df["timestamp"], df["back_x"])

    # test_date_1 = df["timestamp"].values[0]

    # print("date is: {} and is type of: {}".format(test_date_1,type(test_date_1)))

    # format =  "%Y-%m-%d %H:%M:%S.%f"

    # dt_test_1 = datetime.datetime.strptime(test_date_1, format)

    # print("date is: {} and is type of: {}".format(dt_test_1,type(dt_test_1)))

    # print("time is: {}".format(dt_test_1.time()))

    # df["timestamp"] = pd.to_datetime(df["timestamp"], format= format)

    # df["timestamp"] = df["timestamp"].dt.time

    # print("column timestamp {} is now of type {}".format(df["timestamp"].values[0],type(df["timestamp"].values[0])))




    # if(constants.PROCESS):
    #     merged_df = read_data(constants.CSV_PATH, preproc=False)

    #     if not os.path.exists(os.path.join(os.path.dirname(__file__), "/../processed/")):

    #         print("process folder does not exist, creating...")
    #         # If it doesn't exist, create it
    #         os.makedirs(os.path.join(os.path.dirname(__file__), "/../processed/"))

    #     #convert data to csv
    #     merged_df.to_csv(constants.PROC_CSV_PATH + "proc_merged.csv")

    # if(constants.GRAPH):
    #     merged_df = pd.read_csv(constants.PROC_CSV_PATH + "proc_merged.csv")

    #     plotter.plot_gyro(merged_df)

    #     # back_sensor_df, thigh_sensor_df = preproc.separate_sensors(merged_df)

    #     # plot_data = back_sensor_df.loc[:,["timestamp","back_x"]]


if __name__ == "__main__":
    main()