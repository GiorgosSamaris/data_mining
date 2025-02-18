import os
# only declare constants here
CSV_PATH =  os.path.join(os.path.dirname(__file__), "../harth/harth/")
TXT_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output.txt")

#Preprocessing options
PROCESSED_CSV_PATH = os.path.join(os.path.dirname(__file__), "../processed/")
DROP_DATES = 1 
TO_SEC = 2
ADD_SUBJECT_ID = 4
WINDOW_DATA = 8
WRITE_DATA = 16
DROP_NON_UNIFORM_COLUMNS = 32
MERGE = 64
PREPROCESSING_OPTIONS = 0
PREPROCESSING_OPTIONS |=  MERGE | DROP_NON_UNIFORM_COLUMNS | DROP_DATES | TO_SEC | ADD_SUBJECT_ID | WINDOW_DATA

# Console print Options
PRINT_OPTIONS = 0
STATISTICS = 1
# PRINT_OPTIONS |=  STATISTICS


#Plot options
CORRELATION_MATRIX = 1
ACT_AXIS_DISTRIB = 2
PLOT_OPTIONS = 0
# PLOT_OPTIONS |= CORRELATION_MATRIX

#Classification options
CLASSIFICATION_OPTIONS = 0
NAIVE_BAYES = 1
RANDOM_FOREST = 2
MLP_CLASSIFIER = 4

# CLASSIFICATION_OPTIONS |= MLP_CLASSIFIER

#Clustering options
CLUSTERING_OPTIONS = 0
KMEANS = 1
AGGLO = 2
ELBOW_TEST = 4
CLUSTERING_OPTIONS |= KMEANS | AGGLO | ELBOW_TEST

subject_id = {"S006":6, "S008":8, "S009":9, "S010":10, "S012":12, "S013":13, "S014":14, "S015":15, 
              "S016":16, "S017":17, "S018":18, "S019":19, "S020":20, "S021":21, "S022":22, "S023":23,
               "S024":24, "S025":25, "S026":26, "S027":27, "S028":28, "S029":29} 

activity_id = {
    1: "walking", 2: "running", 3: "shuffling", 4: "stairs (ascending)", 5: "stairs (descending)", 6: "standing", 7: "sitting", 8: "lying", 13: "cycling (sit)", 14: "cycling (stand)", 130: "cycling (sit, inactive)", 140: "cycling (stand, inactive)"
}

COLOR_MAP = "tab20"