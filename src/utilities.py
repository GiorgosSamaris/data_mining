import pandas as pd
import numpy as np
import constants
import matplotlib.pyplot as plt

class CSVHandler:

    @staticmethod
    def read_csv(input_file, verbose = False):
        """
        Read a CSV file and return its contents as a pandas DataFrame.
        Parameters:
            input_file (str): The path to the CSV file to be read.
            verbose (bool, optional): If True, print additional information about the DataFrame such as head, description, info, and missing values. Default is False.
        Returns:
            pandas.DataFrame or None: The DataFrame containing the CSV data if the file exists and is not ".gitignore", otherwise returns None.
        """
        if ".gitignore" in input_file:
            return None
        csv_data_frame = pd.read_csv(input_file)
        if verbose:
            print("---------------------------------------------------------------------------------------------\n")
            print("File: {}".format(input_file))
            print(csv_data_frame.head())
            print(csv_data_frame.describe())
            print(csv_data_frame.info())
            print("Missing values: {}".format(csv_data_frame.isnull().sum()))
        return csv_data_frame 
    


class Preprocessing:

    @staticmethod
    def drop_dates(data_frame, timestamp_format = "%Y-%m-%d %H:%M:%S.%f") -> pd.DataFrame:
        """
        Drops the date part from the timestamp column of the DataFrame. 

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame from which columns are to be dropped.
            timestamp_format (str): format of the timestamp as it appears in the orginial DataFrame. Default is "%Y-%m-%d %H:%M:%S.%f".

        Returns:
            pandas.DataFrame: The returned DataFrame only has time on the timestamp column

        """
        #Convert timestamp(str) -> timestamp(numpy.datetime64)
        data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp"])
        #Extract time part from timestamp (Also converts timestamp(numpy.datetime64) -> timestamp(datetime.time))
        data_frame["timestamp"] = data_frame["timestamp"].dt.time
        return data_frame
    
    @staticmethod
    def convert_to_seconds(data_frame) -> pd.DataFrame:
        """
        Converts timestamp column from time format (H:M:S.s) to float seconds. 

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame from which columns are to be dropped.

        Returns:
            pandas.DataFrame: The returned DataFrame only has total time in seconds in timestamp column

        """
        #Convert timestamp(datetime.time) -> timestamp(datetime.timedelta)))
        data_frame["timestamp"] = pd.to_timedelta(data_frame["timestamp"].astype(str))
        #Calculate time in seconds
        data_frame["timestamp"] = data_frame["timestamp"].dt.total_seconds()
        return data_frame

    @staticmethod
    def drop_nonuniform_columns(data_frame, verbose=False) -> pd.DataFrame:
        """
        Drop columns 'index', 'Unnamed: 0' and 'Unknown: 0' from the DataFrame if they exist.

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame from which columns are to be dropped.
            verbose (bool, optional): If True, print a message for each column dropped. Default is False.

        Returns:
            pandas.DataFrame : Altered or unaltered dataframe depending on if it had one (or both) of the columns: 'index' and 'Unknown: 0'
        """
        if "index" in data_frame.columns:
            data_frame.drop(['index'], axis='columns', inplace= True)
            if verbose:
                print("Removed column 'index'")
        if "Unknown: 0" in data_frame.columns:
            data_frame.drop(['Unknown: 0'], axis='columns', inplace= True)
            if verbose:
                print("Removed column 'UnKnown: 0'")
        if "Unnamed: 0" in data_frame.columns:
            data_frame.drop(['Unnamed: 0'], axis='columns', inplace= True)
            if verbose:
                print("Removed column 'Unnamed: 0'")
        return data_frame

    @staticmethod
    def drop_outliers(data_frame, verbose = False):
        """
        Drop outliers from specific columns of the DataFrame using the IQR method.

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame from which outliers are to be dropped.
            verbose (bool, optional): If True, print the size of the DataFrame before and after dropping outliers. Default is False.

        Returns:
            pandas.DataFrame
        """
        if verbose:
            print("Size of file before dropping outliers: {}".format(data_frame.shape))
        for column in ['back_x','back_y','back_z','thigh_x','thigh_y','thigh_z']:
            Q1 = data_frame[column].quantile(0.25)
            Q3 = data_frame[column].quantile(0.75)
            IQR = Q3 - Q1
            threshold = 1.5
            data_frame[(data_frame[column] < Q1 - threshold * IQR) | (data_frame[column] > Q3 + threshold * IQR)] = data_frame[column].median()
        if verbose:
            print("Size of file after dropping outliers: {}".format(data_frame.shape))
        return data_frame

        
    @staticmethod
    def separate_sensors(data_frame):
        """
        Given a data frame it separates sensor readings into to different data frames

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame to be separated on two new dataframes.
        

        Returns:
            back_sensor_data (pandas.DataFrame), thigh_sensor_data (pandas.DataFrame)
        """
        if "subject_id" in data_frame.columns:
            back_sensor_data = data_frame[["timestamp","back_x", "back_y", "back_z", "subject_id"]]
            thigh_sensor_data = data_frame[["timestamp","thigh_x", "thigh_y", "thigh_z", "subject_id"]]
        else:
            back_sensor_data = data_frame[["timestamp","back_x", "back_y", "back_z"]]
            thigh_sensor_data = data_frame[["timestamp","thigh_x", "thigh_y", "thigh_z"]]
        return back_sensor_data, thigh_sensor_data


    @staticmethod
    def add_subject_id(data_frame, file_name, column_pos = 8):
        """
        Given a data frame it separates sensor readings into to different data frames

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame on which the new column containing the sunject id will be added.
            file_name (str): The filename from which the current data frame was created
            column_pos (int): Position of the new column (starts from index 0)
        

        Returns:
            data_frame (pandas.DataFrame)
        """
        #get subject id
        s_name = file_name.split('.')[0]
        s_id = constants.subject_id[s_name]
        data_frame.insert(column_pos, "subject_id", s_id)
        return data_frame

    @staticmethod
    def separate_activities(data_frame):
        """
        Separate classes of each dataframe to new dataframe

        Parameters:
            data_frame (pandas.DataFrame): The DataFrame to be separated.

        Returns:
            dict : A dictionary containing the separated dataframes.
        """
        separated_data = {}
        for i in np.unique(data_frame['label']):
            separated_data[i] = data_frame[data_frame['label'] == i]
        return separated_data
    
    @staticmethod
    def window_data(df_input, window_size = 200, step = 100):
        """
            Process input data frame using rolling window averaging (on motion data columns) and mode (on label and subject_id) calculation.

            Parameters:
            - df_input: Input pandas DataFrame containing motion data.
            - window_size (optional): Size of the rolling window. Default is 200.
            - step (optional): Step size for the rolling window. Default is 100.

            Returns:
            - data_frame: Processed DataFrame containing windowed data.
        """
        df_subset = df_input[['back_x', 'back_y', 'back_z', 'thigh_x', 'thigh_y', 'thigh_z']];
        data_frame = df_subset.rolling(window_size, min_periods = 1, step=step).mean()
        data_frame['label'] = df_input['label'].rolling(window_size, min_periods = 1, step=step).apply(lambda x: x.mode()[0]).astype(int)
        data_frame['variance_back_x'] = df_subset['back_x'].rolling(window_size, min_periods = 1, step=step).var().bfill()
        data_frame['variance_back_y'] = df_subset['back_y'].rolling(window_size, min_periods = 1, step=step).var().bfill()
        data_frame['variance_back_z'] = df_subset['back_z'].rolling(window_size, min_periods = 1, step=step).var().bfill()
        data_frame['variance_thigh_y'] = df_subset['thigh_y'].rolling(window_size, min_periods = 1, step=step).var().bfill()
        data_frame['variance_thigh_z'] = df_subset['thigh_z'].rolling(window_size, min_periods = 1, step=step).var().bfill()
        data_frame['variance_thigh_x'] = df_subset['thigh_x'].rolling(window_size, min_periods = 1, step=step).var().bfill()
        if 'subject_id' in df_input.columns:
            data_frame['subject_id'] = df_input['subject_id'].rolling(window_size, min_periods = 1, step=step).apply(lambda x: x.mode()[0]).astype(int)
        return data_frame
    

    def basic_statistics(df_input, verbose = False):
        columns = ['back_x', 'back_y', 'back_z', 'thigh_x', 'thigh_y', 'thigh_z']
        mean = []
        median = []
        std = []
        min_val = []
        max_val = []
        variance = []
        for col in columns:
            mean.append(df_input[col].mean())
            median.append(df_input[col].median())
            std.append(df_input[col].std())
            min_val.append(df_input[col].min())
            max_val.append(df_input[col].max())
            variance.append(df_input[col].var())
        if verbose:
            print("---------------------------------------------------------------------------------------------\n")
            print("Columns: {}".format(columns))
            print("Mean: {}".format(mean))
            print("Median: {}".format(median))
            print("Standard Deviation: {}".format(std))
            print("Minimum Value: {}".format(min_val))
            print("Maximum Value: {}".format(max_val))
            print("Variance: {}".format(variance))
            print("---------------------------------------------------------------------------------------------\n")
        return mean, median, std, min_val, max_val, variance
    
    

    def group_activities(df_input):
        column_labels = ["subject_id","1","2","3","4","5","6","7","8","13","14","130","140"]
        df_output = pd.DataFrame(columns=column_labels)
        for subject in np.unique(df_input["subject_id"]):
            temp_df = pd.DataFrame(columns=column_labels)
            for label in np.unique(df_input['label']):
                label_duration = df_input[(df_input['subject_id'] == subject) & (df_input['label'] == label)].shape[0] * 0.02
                temp_df[str(label)] = [label_duration]
            temp_df["subject_id"] = subject
            df_output = pd.concat([df_output, temp_df], ignore_index=True)
        return df_output
    
    
    # def activity_time(df_input, verbose = False):
    #     df_output = pd.DataFrame(columns=['subject_id', 'label', 'duration'])
    #     for subject_id in np.unique(df_input['subject_id']):
    #         for label in np.unique(df_input['label']):
    #             duration = df_input[(df_input['subject_id'] == subject_id) & (df_input['label'] == label)].shape[0] * 0.02
    #             temp_df = pd.DataFrame([[subject_id, label, duration]], columns=['subject_id', 'label', 'duration'])
    #             df_output = pd.concat([df_output, temp_df], ignore_index=True)
    #     return df_output


    # def calculate_correlation(df_input, plot = False):
    #     """
    #     Calculate the correlation matrix of the input DataFrame.

    #     Parameters:   
    #         df_input (pandas.DataFrame): The DataFrame for which the correlation matrix is to be calculated.

    #     Returns:
    #         pandas.DataFrame: The correlation matrix of the input DataFrame.
    #     """
    #     corr_matrix = df_input.corr()   
        
    #     if plot:
    #     # Set up the matplotlib figure
    #     plt.figure(figsize=(8, 6))

    #     # Create the heatmap using imshow
    #     plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)

    #     # Add color bar
    #     plt.colorbar()

    #     # Add titles and labels
    #     plt.title('Correlation Matrix Heatmap')

    #     # Set x and y ticks
    #     plt.xticks(ticks=np.arange(len(corr_matrix.columns)), labels=corr_matrix.columns)
    #     plt.yticks(ticks=np.arange(len(corr_matrix.columns)), labels=corr_matrix.columns)

    #     # Rotate the x labels for better readability
    #     plt.xticks(rotation=45)

    #     # Add the correlation values as annotations
    #     for i in range(len(corr_matrix.columns)):
    #         for j in range(len(corr_matrix.columns)):
    #             plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', ha='center', va='center', color='black')

    #     # Display the plot
    #     plt.show()
    #     return 