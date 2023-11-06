import pandas as pd

import json

def combine_two_json_files(file1, file2):
    with open(file1, 'r') as f1:
        dict1 = json.load(f1)
    with open(file2, 'r') as f2:
        dict2 = json.load(f2)
    combined_dict = {**dict1, **dict2}
    sorted_dict = {key: combined_dict[key] for key in sorted(combined_dict)}
    return sorted_dict

def combine_two_csv_files(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    combined_df = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    return combined_df