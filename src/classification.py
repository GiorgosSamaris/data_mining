import utilities as utils
import constants
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import naive_bayes as nb 
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


class Classifiers:
    def __init__(self) -> None:
        pass

    @staticmethod
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
        cm = confusion_matrix(y_test, y_preds, labels=model.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
        disp.plot()
        plt.show()
        # normalize and plot confusion matrix
        norm_cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        disp = ConfusionMatrixDisplay(confusion_matrix=norm_cm, display_labels=model.classes_)
        disp.plot()
        plt.show()
        # Evaluate the model and append its score to model_scores
        #return model.score(X_test, y_test)
        metric_dict = {
        'accuracy_score' : accuracy_score(y_test, y_preds),
        'precision_score' : precision_score(y_test, y_preds, average='weighted', labels=np.unique(y_preds)),
        'recall_score' : recall_score(y_test, y_preds, average='weighted'),
        'f1_score' : f1_score(y_test, y_preds, average='weighted')
        }
        return metric_dict