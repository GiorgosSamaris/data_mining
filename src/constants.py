import os
# only declare constants here
CSV_PATH =  os.path.join(os.path.dirname(__file__), "../harth/harth/")
TXT_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output.txt")

subject_id = {"S006":6, "S008":8, "S009":9, "S010":10, "S012":12, "S013":13, "S014":14, "S015":15, 
              "S016":16, "S017":17, "S018":18, "S019":19, "S020":20, "S021":21, "S022":22, "S023":23,
               "S024":24, "S025":25, "S026":26, "S027":27, "S028":28, "S029":29} 

activity_id = {
    1: "walking", 2: "running", 3: "shuffling", 4: "stairs (ascending)", 5: "stairs (descending)", 6: "standing", 7: "sitting", 8: "lying", 13: "cycling (sit)", 14: "cycling (stand)", 130: "cycling (sit, inactive)", 40: "cycling (stand, inactive)"
}