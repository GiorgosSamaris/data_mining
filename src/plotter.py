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
    plt.legend([(constants.activity_id[i], i) for i in unique_activities], loc='best', fontsize = 5)
    plt.show()
    return

def activity_histogram(df_input):
    activity_ids = df_input['label']
    unique_activities, num_examples_per_activity = np.unique(activity_ids, return_counts = True)
    plt.hist(activity_ids, bins = len(unique_activities), range=[0, len(unique_activities)], align='mid', edgecolor='black', linewidth=1)
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