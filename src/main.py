import pandas as pd
import os 
import plotter
from classification import Classifiers 
import constants
from utilities import CSVHandler as csv
from utilities import Preprocessing as preproc
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import numpy as np
def read_data(file_path = ".") -> dict[pd.DataFrame]:
    dataframes = {}
    
    for file in os.listdir(file_path):
        temp_df = csv.read_csv(file_path+file)
        if temp_df is None:
            continue
        
        dataframes[file] = temp_df

    return dataframes

def main():
    dataframes_dict = read_data(constants.CSV_PATH)
    homogeneous_df = pd.DataFrame()
    cluster_homogeneous_df = pd.DataFrame()

    #Read/Preproc/Merge
    for key in dataframes_dict:
        df = dataframes_dict[key]       
        if constants.PREPROCESSING_OPTIONS & 1 == constants.DROP_DATES:
            df = preproc.drop_dates(data_frame=df)
        if constants.PREPROCESSING_OPTIONS & 2 == constants.TO_SEC:
            df = preproc.convert_to_seconds(data_frame=df)
        if constants.PREPROCESSING_OPTIONS & 4 == constants.ADD_SUBJECT_ID:
            df = preproc.add_subject_id(data_frame=df, file_name = key, column_pos=8)
        if constants.PREPROCESSING_OPTIONS & 8 == constants.WINDOW_DATA:
            cluster_df = df.copy()
            df = preproc.window_data(df_input=df, window_size=200)
        if constants.PREPROCESSING_OPTIONS & 16 == constants.WRITE_DATA:
            pass
        if constants.PREPROCESSING_OPTIONS & 32 == constants.DROP_NON_UNIFORM_COLUMNS:
            cluster_df = preproc.drop_nonuniform_columns(cluster_df)
            df = preproc.drop_nonuniform_columns(df)
        if constants.PREPROCESSING_OPTIONS & 64 == constants.MERGE:
            cluster_homogeneous_df = pd.concat([cluster_homogeneous_df, cluster_df])
            homogeneous_df = pd.concat([homogeneous_df, df])
    
    # print statistics per activity_id
    if constants.PRINT_OPTIONS & 1 == constants.STATISTICS:
        for activity_id in homogeneous_df["label"].unique():
            print(f"Activity ID: {activity_id}")
            print(preproc.basic_statistics(homogeneous_df[homogeneous_df["label"] == activity_id]))

    #Plotting
    if constants.PLOT_OPTIONS & 1 == constants.CORRELATION_MATRIX:
        corr_matrix = homogeneous_df.corr()[:6,:6]
        plotter.plot_corr_matrix(corr_matrix)
    if constants.PLOT_OPTIONS & 2 == constants.ACT_AXIS_DISTRIB:
        for activity_id in homogeneous_df["label"].unique():
            plotter.plot_activity_axis_distribution(homogeneous_df, activity_id)
    
    #Classification
    X = homogeneous_df[["thigh_x", 'back_x', 'thigh_y', 'back_y', 'thigh_z', 'back_z', 'variance_back_x', 'variance_back_y', 'variance_back_z', 'variance_thigh_x', 'variance_thigh_y', 'variance_thigh_z']]
    Y = homogeneous_df[["label"]]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
    if constants.CLASSIFICATION_OPTIONS & 1 == constants.NAIVE_BAYES:
        model = GaussianNB()
        print(Classifiers.get_metrics(model,X_train,X_test,y_train,y_test))
    if constants.CLASSIFICATION_OPTIONS & 2 == constants.RANDOM_FOREST:
        model = RandomForestClassifier(criterion='gini',n_estimators=10)
        print(Classifiers.get_metrics(model,X_train,X_test,y_train,y_test))
    if constants.CLASSIFICATION_OPTIONS & 4 == constants.MLP_CLASSIFIER:
        model = MLPClassifier(activation='relu',hidden_layer_sizes=(22,))
        print(Classifiers.get_metrics(model,X_train,X_test,y_train,y_test))

# CLUSTERING
    grouped_df = preproc.group_activities(cluster_homogeneous_df)
    scaled_df = pd.DataFrame(StandardScaler().fit_transform(grouped_df.iloc[:, 1:]), columns=grouped_df.columns[1:], index=grouped_df.index)
    if constants.CLUSTERING_OPTIONS & 1 == constants.KMEANS:
        k_means = KMeans(n_clusters=2)
        k_means.fit(scaled_df)
        grouped_df["cluster"] = k_means.labels_
        cluster_0 = grouped_df[grouped_df["cluster"] == 0]
        cluster_1 = grouped_df[grouped_df["cluster"] == 1]
        cluster_0_avg = pd.DataFrame(cluster_0.iloc[:,1:-1].mean()).transpose()
        cluster_0_avg.columns = cluster_0.columns[1:-1]
        cluster_1_avg = pd.DataFrame(cluster_1.iloc[:,1:-1].mean()).transpose()
        cluster_1_avg.columns = cluster_1.columns[1:-1]
        fig,ax = plt.subplots(2,1)
        ax[0].barh(cluster_0_avg.columns, cluster_0_avg.iloc[0], color='blue', label='Cluster 0')
        ax[1].barh(cluster_1_avg.columns, cluster_1_avg.iloc[0], color='red', label='Cluster 1')
        plt.xlabel('Value')
        plt.ylabel('Column')
        plt.legend()
        plt.show()

    if constants.CLUSTERING_OPTIONS & 4 == constants.ELBOW_TEST:
        wcss = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(grouped_df)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1, 11), wcss, marker='o')
        plt.show()


    if constants.CLUSTERING_OPTIONS & 2 == constants.AGGLO:
        agglo = AgglomerativeClustering(n_clusters=3)
        agglo.fit(scaled_df)
        labels = agglo.labels_
        grouped_df["cluster"] = labels
        cluster_0 = grouped_df[grouped_df["cluster"] == 0]
        cluster_1 = grouped_df[grouped_df["cluster"] == 1]
        cluster_2 = grouped_df[grouped_df["cluster"] == 2]
        cluster_0_avg = pd.DataFrame(cluster_0.iloc[:,1:-1].mean()).transpose()
        cluster_0_avg.columns = cluster_0.columns[1:-1]
        cluster_1_avg = pd.DataFrame(cluster_1.iloc[:,1:-1].mean()).transpose()
        cluster_1_avg.columns = cluster_1.columns[1:-1]
        cluster_2_avg = pd.DataFrame(cluster_2.iloc[:,1:-1].mean()).transpose()
        cluster_2_avg.columns = cluster_2.columns[1:-1]
        fig,ax = plt.subplots(3,1)
        ax[0].barh(cluster_0_avg.columns, cluster_0_avg.iloc[0], color='blue', label='Cluster 0')
        ax[1].barh(cluster_1_avg.columns, cluster_1_avg.iloc[0], color='red', label='Cluster 1')
        ax[2].barh(cluster_2_avg.columns, cluster_2_avg.iloc[0], color='red', label='Cluster 2')
        plt.xlabel('Value')
        plt.ylabel('Column')
        plt.legend()
        plt.show()
        scores = []
        range_values = range(2, 10)
        for i in range_values:
            model = AgglomerativeClustering(n_clusters=i)
            labels = model.fit_predict(scaled_df)
            scores.append(silhouette_score(scaled_df, labels))
        plt.plot(range_values, scores, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Silhouette Score')
        plt.show()
    
if __name__ == "__main__":
    main()