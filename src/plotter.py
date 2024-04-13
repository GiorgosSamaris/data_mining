from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import constants
import pandas as pd



def activity_pie (df_input):
    activity_ids = df_input['label']
    unique_activities, num_examples_per_activity = np.unique(activity_ids, return_counts = True)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    cmap = plt.get_cmap("tab20")
    sampled_colors = [cmap(i) for i in range (len(num_examples_per_activity))]
    ax.pie(x = num_examples_per_activity, 
            colors = sampled_colors,
            labels = unique_activities, 
            wedgeprops= {'linewidth': 1, 'edgecolor': 'black'}, 
            textprops = {'size': 'medium', 'family': "monospace", 'weight': 'medium'},
            autopct = '%1.3f%%'
    );
    plt.legend([(constants.activity_id[i], i) for i in unique_activities], loc='best', fontsize = 5)
    plt.show()
    return

def activity_histogram(df_input):
    activity_ids = df_input['label']
    unique_activities, num_examples_per_activity = np.unique(activity_ids, return_counts = True)
    plt.hist(activity_ids, bins = len(unique_activities), range=[0, len(unique_activities)], align='mid', edgecolor='black', linewidth=1)
    plt.title("Subject "+str(df_input['subject_id'][1]))
    plt.show()
    return

def plot_accel(df_input):
    fig, ax = plt.subplots(nrows=2, ncols=1)
    ax[0].plot(df_input['back_x'], label='back_x')
    ax[0].plot(df_input['back_y'], label='back_y')
    ax[0].plot(df_input['back_z'], label='back_z')
    ax[0].set_title("Back Sensor Data")
    ax[0].set_ylabel("Accel Data")
    ax[0].legend(loc='best')
    ax[1].plot(df_input['thigh_x'], label='thigh_x')
    ax[1].plot(df_input['thigh_y'], label='thigh_y')
    ax[1].plot(df_input['thigh_z'], label='thigh_z')
    ax[1].set_title("Thigh Sensor Data")
    ax[1].set_ylabel("Accel Data")
    ax[1].legend(loc='best')
    plt.show()

# plot distribuiton of each sensor, back_x, back_y, back_z, thigh_x, thigh_y, thigh_z
def sensor_distribution(df_input):
    fig, ax = plt.subplots(nrows=2, ncols=3)
    ax[0,0].hist(df_input['back_x'], bins=100, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[0,0].set_title("Back Sensor X")
    ax[0,1].hist(df_input['back_y'], bins=100, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[0,1].set_title("Back Sensor Y")
    ax[0,2].hist(df_input['back_z'], bins=100, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[0,2].set_title("Back Sensor Z")
    ax[1,0].hist(df_input['thigh_x'], bins=100, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[1,0].set_title("Thigh Sensor X")
    ax[1,1].hist(df_input['thigh_y'], bins=100, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[1,1].set_title("Thigh Sensor Y")
    ax[1,2].hist(df_input['thigh_z'], bins=100, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[1,2].set_title("Thigh Sensor Z")
    plt.show()
    return


def plot_activity_axis_distribution(df_input, activity_id):
    df_input = df_input[df_input['label'] == activity_id]
    fig, ax = plt.subplots(nrows=2, ncols=3)
    ax[0,0].hist(df_input['back_x'], bins=1000, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[0,0].set_title("Back Sensor X")
    ax[0,1].hist(df_input['back_y'], bins=1000, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[0,1].set_title("Back Sensor Y")
    ax[0,2].hist(df_input['back_z'], bins=1000, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[0,2].set_title("Back Sensor Z")
    ax[1,0].hist(df_input['thigh_x'], bins=1000, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[1,0].set_title("Thigh Sensor X")
    ax[1,1].hist(df_input['thigh_y'], bins=1000, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[1,1].set_title("Thigh Sensor Y")
    ax[1,2].hist(df_input['thigh_z'], bins=1000, range=[-1.5, 1.5], align='mid', edgecolor='black', linewidth=1)
    ax[1,2].set_title("Thigh Sensor Z")
    fig.suptitle(constants.activity_id[activity_id])
    plt.show()
    return

    

@staticmethod
def plot_timeseries(df_input: pd.DataFrame, column_label: str | list[str], axes: plt.axes = None, **kwargs) -> plt.axes:

    """
        Plot specified columns for given dataframe. IMPORTANT: pyplot.show() still needed to show the plotted data

        Parameters:
            - df_input: Input pandas DataFrame containing motion data.
            - column_label: Label of column containing the data to be plotted in respect to time

        Optional Parameters:
            - axes (Default = None): Axes on which the data will be plotted. In case of none create new axes on function call
            - color: Color with which the data point will be plotted. By default color will be alternated. The color pallete depends on constants.COLOR_MAP
            - time_column: In case another label is used than 'timestamp' 
            - title: Title of the axes. By default column_label parameter is used as a name

        Returns:
            Any
    """
    #Init static var rotating_index 
    if not hasattr(plot_timeseries, "rotating_index"):
        plot_timeseries.rotating_index = 0
        

    if axes == None:
        figure, axes = plt.subplots()

    time_column = kwargs.get('time_column', "timestamp")    #In case a custom label for time column is used
    title = kwargs.get('title', column_label)

    #Use rotating color palette unless stated otherwise
    cmap = cm.get_cmap(constants.COLOR_MAP).colors
    plot_timeseries.rotating_index += 1 % len(cmap)
    color = kwargs.get('color', cmap[plot_timeseries.rotating_index])


    axes.plot(df_input[time_column], df_input[column_label],color = color)
    axes.set_title(title)

    return



    
