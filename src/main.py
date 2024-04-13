import pandas as pd
import os 
import plotter
import constants
from utilities import CSVHandler as csv
from utilities import Preprocessing as preproc
import matplotlib.pyplot as plt
from sklearn import naive_bayes as nb 
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import numpy as np
def read_data(file_path = ".") -> dict[pd.DataFrame]:
    dataframes = {}
    
    for file in os.listdir(file_path):
        temp_df = csv.read_csv(file_path+file)
        if temp_df is None:
            continue
        
        dataframes[file] = temp_df

    return dataframes

def get_metrics(model, X_train, X_test, y_train, y_test):
    """
    Fits and evaluates given machine learning model.
    model : Scikit-Learn machine learning model
    X_train : training data
    X_test : testing data
    y_train : training labels
    y_test : test labels
    """
    # Set random seed
    np.random.seed(42)
    # Fit the model to the data
    model.fit(X_train, y_train)
    # Get Predictions
    y_preds = model.predict(X_test)
    # Evaluate the model and append its score to model_scores
    #return model.score(X_test, y_test)
    metric_dict = {
    'accuracy_score' : accuracy_score(y_test, y_preds),
    'precision_score' : precision_score(y_test, y_preds, average='weighted', labels=np.unique(y_preds)),
    'recall_score' : recall_score(y_test, y_preds),
    'f1_score' : f1_score(y_test, y_preds),
    'roc_auc_score' : roc_auc_score(y_test, y_preds),
    }
    return metric_dict


def main():
    dataframes_dict = read_data(constants.PROCESSED_CSV_PATH)
    homogeneous_df = pd.DataFrame()
    for key in dataframes_dict:
        df = dataframes_dict[key]
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
        if constants.OPTIONS & 32 == constants.DROP_NON_UNIFORM_COLUMNS:
            df = preproc.drop_nonuniform_columns(df)
        if constants.OPTIONS & 64 == constants.MERGE:
            homogeneous_df = pd.concat([homogeneous_df,df])
    
    X = homogeneous_df[['thigh_x', 'back_x']]
    Y = homogeneous_df[['label']]
    X_train, X_test, y_train, y_test = train_test_split(np.transpose(X.to_numpy()),np.transpose(Y.to_numpy()),test_size=0.2)
    
    model = GaussianNB()
    print(get_metrics(model,X_train,X_test,y_train,y_test))
if __name__ == "__main__":
    main()