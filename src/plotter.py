from matplotlib import pyplot as plt
import numpy as np
import constants

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
    plt.title("Subject "+str(df_input['subject_id'][1]))
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

def plot_gyro(df_input):
    fig, ax = plt.subplots(nrows=2, ncols=1)
    ax[0].plot(df_input['back_x'], label='back_x')
    ax[0].plot(df_input['back_y'], label='back_y')
    ax[0].plot(df_input['back_z'], label='back_z')
    ax[0].set_title("Back Sensor Data")
    ax[0].set_ylabel("Gyro Data")
    ax[0].legend(loc='best')
    ax[1].plot(df_input['thigh_x'], label='thigh_x')
    ax[1].plot(df_input['thigh_y'], label='thigh_y')
    ax[1].plot(df_input['thigh_z'], label='thigh_z')
    ax[1].set_title("Thigh Sensor Data")
    ax[1].set_ylabel("Gyro Data")
    ax[1].legend(loc='best')
    plt.show()