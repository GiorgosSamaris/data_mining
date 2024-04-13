import pandas as pd
import os 
import plotter
import constants
from utilities import CSVHandler as csv
from utilities import Preprocessing as preproc
import matplotlib.pyplot as plt

def read_data(file_path = ".") -> dict[pd.DataFrame]:

    dataframes = {}

    for file in os.listdir(file_path):
        temp_df = csv.read_csv(file)
        if temp_df is None:
            continue

        dataframes[file] = temp_df

    return dataframes




def main():


    dataframes = read_data(constants.PROCESSED_CSV_PATH)

    for key in dataframes:

        df = dataframes[key]

        if constants.OPTIONS & 1 == constants.DROP_DATES:
            df = preproc.drop_dates(data_frame=df)

        if constants.OPTIONS & 2 == constants.TO_SEC:
            df = preproc.convert_to_seconds(data_frame=df)

        if constants.OPTIONS & 4 == constants.ADD_SUBJECT_ID:
            df = preproc.add_subject_id(data_frame=df, file_name = key, column_pos=8)

        if constants.OPTIONS & 8 == constants.WINDOW_DATA:
            df = preproc.window_data(df_input=df, window_size=200)

        if constants.OPTIONS & 16 == constants.WRITE_DATA:
           pass



if __name__ == "__main__":
    main()